//! Preliminary spatial vocabulary, freshly written for the independent game.
//!
//! Y is up; rooms will occupy X/Z footprints at a selected surface height.
//! These types are not a save format or an engine integration. No terrain store,
//! renderer, content loader, or gameplay is implemented in Phase 0.

/// Provisional chunk edge for addressing experiments, not a frozen file ABI.
pub const CHUNK_EDGE: i32 = 16;

/// A cubic cell in world space, including negative coordinates.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub struct VoxelPos {
    pub x: i32,
    pub y: i32,
    pub z: i32,
}

/// A chunk in the same three axes as world space.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub struct ChunkPos {
    pub x: i32,
    pub y: i32,
    pub z: i32,
}

/// An in-chunk cell. Private fields enforce coordinates in 0..CHUNK_EDGE.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub struct LocalPos {
    x: u8,
    y: u8,
    z: u8,
}

impl LocalPos {
    /// Reject a coordinate outside this provisional chunk size.
    pub fn new(x: u8, y: u8, z: u8) -> Option<Self> {
        if [x, y, z].into_iter().all(|v| i32::from(v) < CHUNK_EDGE) {
            Some(Self { x, y, z })
        } else {
            None
        }
    }

    pub fn xyz(self) -> [u8; 3] {
        [self.x, self.y, self.z]
    }

    /// X changes fastest, then Z, then Y; see the draft native map spec.
    pub fn linear_index(self) -> usize {
        let edge = CHUNK_EDGE as usize;
        usize::from(self.x) + edge * (usize::from(self.z) + edge * usize::from(self.y))
    }
}

impl VoxelPos {
    /// Euclidean division keeps local coordinates positive west/below the origin.
    pub fn split(self) -> (ChunkPos, LocalPos) {
        (
            ChunkPos {
                x: self.x.div_euclid(CHUNK_EDGE),
                y: self.y.div_euclid(CHUNK_EDGE),
                z: self.z.div_euclid(CHUNK_EDGE),
            },
            LocalPos {
                x: self.x.rem_euclid(CHUNK_EDGE) as u8,
                y: self.y.rem_euclid(CHUNK_EDGE) as u8,
                z: self.z.rem_euclid(CHUNK_EDGE) as u8,
            },
        )
    }
}

impl ChunkPos {
    /// Return None for a chunk/local combination outside the world i32 range.
    pub fn voxel(self, local: LocalPos) -> Option<VoxelPos> {
        fn axis(chunk: i32, local: u8) -> Option<i32> {
            // Widen first: a valid final coordinate must not overflow midway.
            i32::try_from(i64::from(chunk) * i64::from(CHUNK_EDGE) + i64::from(local)).ok()
        }
        Some(VoxelPos {
            x: axis(self.x, local.x)?,
            y: axis(self.y, local.y)?,
            z: axis(self.z, local.z)?,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn negative_boundary_uses_previous_chunk() {
        let (chunk, local) = VoxelPos {
            x: -1,
            y: -16,
            z: 16,
        }
        .split();
        assert_eq!(chunk, ChunkPos { x: -1, y: -1, z: 1 });
        assert_eq!(local.xyz(), [15, 0, 0]);
    }

    #[test]
    fn world_range_round_trips_across_all_axes() {
        let cases = [i32::MIN, -17, -16, -1, 0, 15, 16, 17, i32::MAX];
        for x in cases {
            for y in cases {
                for z in cases {
                    let pos = VoxelPos { x, y, z };
                    let (chunk, local) = pos.split();
                    assert_eq!(chunk.voxel(local), Some(pos));
                }
            }
        }
    }

    #[test]
    fn local_range_and_array_order_are_unambiguous() {
        assert!(LocalPos::new(16, 0, 0).is_none());
        assert!(LocalPos::new(0, 16, 0).is_none());
        assert!(LocalPos::new(0, 0, 16).is_none());
        assert_eq!(LocalPos::new(1, 0, 0).unwrap().linear_index(), 1);
        assert_eq!(LocalPos::new(0, 0, 1).unwrap().linear_index(), 16);
        assert_eq!(LocalPos::new(0, 1, 0).unwrap().linear_index(), 256);
        assert_eq!(LocalPos::new(15, 15, 15).unwrap().linear_index(), 4095);
    }

    #[test]
    fn arbitrary_chunk_coordinates_cannot_overflow() {
        let local = LocalPos::new(0, 0, 0).unwrap();
        assert_eq!(
            ChunkPos {
                x: i32::MAX,
                y: 0,
                z: 0
            }
            .voxel(local),
            None
        );
        assert_eq!(
            ChunkPos {
                x: 0,
                y: i32::MIN,
                z: 0
            }
            .voxel(local),
            None
        );
        assert_eq!(
            ChunkPos {
                x: 0,
                y: 0,
                z: i32::MAX
            }
            .voxel(local),
            None
        );
    }
}
