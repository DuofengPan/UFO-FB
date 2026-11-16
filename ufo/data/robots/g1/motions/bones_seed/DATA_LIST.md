# BONES-SEED G1 训练精选集

从1,000条保留 600 条；248 个命名动作家族，总时长 73.9 分钟。已查看的50条全部保留，未使用官方模型的通过/未通过标签删数据。

先保证家族覆盖，再基于关节时序、根部运动和既有FK特征去除较重复版本。左右手、前后方向和高低位置等不同命名家族保持覆盖；重复较多的家族设自适应上限。描述距离仅用于相似度排序，不能解释成关节误差或物理可行性阈值。

明确依赖外部支撑或非目标训练动作的排除数量：8。原始1,000条文件完整保留；删除清单和最近保留项见 removed.json。新CSV仍为硬链接。

## 蹲与低姿态：132 条

### patches_crouch_R_002__A431
- 说明：A person standing upright transitions into a slavic crouching position with knees deeply bent outward and then stands upright, facing forward.
- 名称：patches_crouch_R；时长 12.28s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230713/patches_crouch_R_002__A431.csv`

### crouch_cupboard_low_out_mid_loot_R_002__A297
- 说明：A person in a crouched stance opens the cupboard door with right hand, picks up an item with left hand from a low shelf, places it on the middle shelf, sways their left hand sideways inside the cupboard, then closes the door.
- 名称：crouch_cupboard_low_out_mid_loot_R；时长 10.59s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230322/crouch_cupboard_low_out_mid_loot_R_002__A297.csv`

### crouch_walk_forward_and_back_turn_360_to_idle_R_002__A493
- 说明：A person walks forward in a crouched stance, turns back and walks forward, and returns back to the starting point.
- 名称：crouch_walk_forward_and_back_turn_360_to_idle_R；时长 19.07s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231024/crouch_walk_forward_and_back_turn_360_to_idle_R_002__A493.csv`

### squat_003__A362
- 说明：A person squats three times, then stands idle in an upright posture, facing forward.
- 名称：squat；时长 7.91s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230509/squat_003__A362.csv`

### item_pick_up_crouch_idle_R_001__A353
- 说明：A person standing in a crouching position is picking up an item from the ground with their right hand.
- 名称：item_pick_up_crouch_idle_R；时长 4.20s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230425/item_pick_up_crouch_idle_R_001__A353.csv`

### crouch_ff_stop_180_R_001__A196
- 说明：A crouched person walks forward and then stands for a while.
- 名称：crouch_ff_stop_180_R；时长 9.00s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_stop_180_R_001__A196.csv`

### crouch_ff_loop_270_002__A128
- 说明：A crouched person slowly and unsteadily walks sideways to their right.
- 名称：crouch_ff_loop_270_R；时长 4.03s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230119/crouch_ff_loop_270_002__A128.csv`

### crouch_ff_loop_180_R_003__A145
- 说明：A person maintains a crouched posture and walks slowly and steadily while facing forward.
- 名称：crouch_ff_loop_180_R；时长 5.19s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230125/crouch_ff_loop_180_R_003__A145.csv`

### crouch_cupboard_mid_in_R_004__A291
- 说明：A person is putting something into the medium-height cupboard while crouching.
- 名称：crouch_operating_cupboard_mid_in_R；时长 6.63s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230320/crouch_cupboard_mid_in_R_004__A291.csv`

### yawn_R_walk_ff_start_360_R_crouch_idle_R_002__A472
- 说明：A standing person yawns, then steps backward and gradually lowers into a complete crouch position.
- 名称：yawn_R_walk_ff_start_360_R_crouch_idle_R；时长 10.78s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231010/yawn_R_walk_ff_start_360_R_crouch_idle_R_002__A472.csv`

### crouch_turn_270_R_001__A244
- 说明：A person turns right while in a crouched position.
- 名称：crouch_turn_270_R；时长 4.02s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：屈膝低姿态、躯干前倾、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_turn_270_R_001__A244.csv`

### crouch_operating_cupboard_low_in_R_004__A298
- 说明：A person in a crouched position puts something in a cupboard with both their hands, then stands idle.
- 名称：crouch_operating_cupboard_low_in_R；时长 5.93s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230322/crouch_operating_cupboard_low_in_R_004__A298.csv`

### crouch_ff_start_315_R_003__A247
- 说明：A person crouched down starts walking to their right back diagonal direction.
- 名称：crouch_ff_start_315_R；时长 6.55s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_ff_start_315_R_003__A247.csv`

### crouch_ff_stop_225_R_002__A197
- 说明：A person crouching diagonally to the right comes to a stop.
- 名称：crouch_ff_stop_225_R；时长 7.37s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_stop_225_R_002__A197.csv`

### Trusting_stoop_down_005__A057
- 说明：A person picks up an object while walking and then stops.
- 名称：trusting_stoop_down；时长 9.06s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾
- CSV：`curated_600/motions/g1/csv/211117/Trusting_stoop_down_005__A057.csv`

### crouch_ff_start_180_R_003__A197
- 说明：A crouched person starts to walk forward at a slow pace.
- 名称：crouch_ff_start_180_R；时长 4.66s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_start_180_R_003__A197.csv`

### crouch_idle_to_crouch_idle_right_R_001__A246
- 说明：A person in a crouching position takes a step and places the right leg forward while maintaining the stance.
- 名称：crouch_idle_to_crouch_idle_right_R；时长 3.74s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_idle_to_crouch_idle_right_R_001__A246.csv`

### crouch_ff_stop_270_001__A126
- 说明：A person walks sideways to the right in a crouched posture, coordinating arm and leg movements, and gradually comes to a stop.
- 名称：crouch_ff_stop_270_R；时长 11.07s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230119/crouch_ff_stop_270_001__A126.csv`

### crouch_idle_right_R_jogging_ff_start_225_R_walk_arc_cw_start_R_003__A475
- 说明：A person rises from a crouched position, jogs to their right, then walks diagonally to the right before continuing to walk in a clockwise direction.
- 名称：crouch_idle_right_R_jogging_ff_start_225_R_walk_arc_cw_start_R；时长 8.07s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231010/crouch_idle_right_R_jogging_ff_start_225_R_walk_arc_cw_start_R_003__A475.csv`

### crouch_ff_start_270_R_002__A197
- 说明：A person crouch-walks in a cross-stepping manner. Then they gradually stand upright as they continue moving to the right.
- 名称：crouch_ff_start_270_R；时长 5.63s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_start_270_R_002__A197.csv`

### crouch_ff_start_225_R_002__A245
- 说明：A person steadily walks while crouched in the right diagonal direction.
- 名称：crouch_ff_start_225_R；时长 5.62s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_ff_start_225_R_002__A245.csv`

### crouch_ff_loop_360_R_002__A196
- 说明：A person with a slightly crouched stance walks backwards with heavy steps.
- 名称：crouch_ff_loop_360_R；时长 6.25s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_loop_360_R_002__A196.csv`

### crouch_walk_forward_and_back_turn_360_to_idle_R_002__A494
- 说明：A person crouches and walks forward right diagonally steadily, turns around from the right, reaches the starting point, and faces forward.
- 名称：crouch_walk_forward_and_back_turn_360_to_idle_R；时长 19.07s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231024/crouch_walk_forward_and_back_turn_360_to_idle_R_002__A494.csv`

### idle_crouch_loop_001__A198
- 说明：A person is standing in a crouched position.
- 名称：crouch_idle；时长 9.62s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/idle_crouch_loop_001__A198.csv`

### Relaxed_stoop_down_006__A057
- 说明：A person walking forward, relaxed and calm, leans down to pick up an object from the ground.
- 名称：relaxed_stoop_down_R；时长 11.02s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸
- CSV：`curated_600/motions/g1/csv/211117/Relaxed_stoop_down_006__A057.csv`

### item_pick_up_crouch_idle_R_003__A414
- 说明：A crouched person while picks up an item from the ground with their right hand and maintains the crouching position while holding it.
- 名称：item_pick_up_crouch_idle_R；时长 3.23s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230530/item_pick_up_crouch_idle_R_003__A414.csv`

### yawn_R_walk_ff_start_360_R_crouch_idle_R_002__A473
- 说明：A tired person yawns, walks backward, and eventually settles down in a crouching position.
- 名称：yawn_R_walk_ff_start_360_R_crouch_idle_R；时长 10.78s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231010/yawn_R_walk_ff_start_360_R_crouch_idle_R_002__A473.csv`

### crouch_turn_270_R_003__A247
- 说明：A person standing in a crouching position while leaning forward quickly turns to their right and stands still, maintaining the same position.
- 名称：crouch_turn_270_R；时长 4.24s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_turn_270_R_003__A247.csv`

### squat_003__A361
- 说明：A person is performing squats by lifting their arms in the forward direction at a medium pace.
- 名称：squat；时长 8.47s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230509/squat_003__A361.csv`

### idle_crouch_to_idle_crouch_right_R_003__A198
- 说明：A person places the right leg forward while in a crouching position.
- 名称：crouch_idle_to_crouch_idle_right_R；时长 4.00s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/idle_crouch_to_idle_crouch_right_R_003__A198.csv`

### neutral_stoop_down_R_002__A074
- 说明：A person slowly walking forward picks up an object from the ground with their right hand, then walks forward and stands upright.
- 名称：stoop_down_R；时长 6.80s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾
- CSV：`curated_600/motions/g1/csv/221128/neutral_stoop_down_R_002__A074.csv`

### crouch_ff_loop_180_R_003__A146
- 说明：A person maintains a crouched posture and walks slowly and steadily while facing forward.
- 名称：crouch_ff_loop_180_R；时长 5.19s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230125/crouch_ff_loop_180_R_003__A146.csv`

### crouch_ff_stop_360_R_003__A246
- 说明：The person in a crouched stance moves backward while facing forward.
- 名称：crouch_ff_stop_360_R；时长 7.68s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_ff_stop_360_R_003__A246.csv`

### crouch_operating_cupboard_mid_out_R_002__A290
- 说明：A person extends and retracts their hands thrice while maintaining the crouched posture.
- 名称：crouch_operating_cupboard_mid_out_R；时长 5.78s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230320/crouch_operating_cupboard_mid_out_R_002__A290.csv`

### turn_crouch_360_R_002__A196
- 说明：A person turns back over the right shoulder in a couching stance.
- 名称：crouch_turn_360_R；时长 4.16s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/turn_crouch_360_R_002__A196.csv`

### crouch_ff_stop_225_R_002__A247
- 说明：A person crouching diagonally to the right comes to a stop.
- 名称：crouch_ff_stop_225_R；时长 9.09s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_ff_stop_225_R_002__A247.csv`

### crouch_ff_start_180_R_003__A198
- 说明：A crouched person starts to walk forward at a slow pace.
- 名称：crouch_ff_start_180_R；时长 4.63s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_start_180_R_003__A198.csv`

### crouch_ff_loop_315_R_001__A197
- 说明：A crouched person walks sideways one step at a time to the right.
- 名称：crouch_ff_loop_315_R；时长 5.61s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_loop_315_R_001__A197.csv`

### crouch_ff_stop_270_R_002__A247
- 说明：A person in a crouching stance walks sideways towards their right and then stays idle in the crouching stance.
- 名称：crouch_ff_stop_270_R；时长 7.06s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_ff_stop_270_R_002__A247.csv`

### crouch_ff_stop_315_R_001__A197
- 说明：A person in a crouched position moving sideways to the right back diagonal comes to a stop.
- 名称：crouch_ff_stop_315_R；时长 6.42s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_stop_315_R_001__A197.csv`

### crouch_ff_start_225_R_001__A247
- 说明：A person steadily walks while crouched in the right diagonal direction.
- 名称：crouch_ff_start_225_R；时长 5.10s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_ff_start_225_R_001__A247.csv`

### crouch_ff_loop_225_R_001__A247
- 说明：A crouched person walks forward at a slow pace.
- 名称：crouch_ff_loop_225_R；时长 5.43s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_ff_loop_225_R_001__A247.csv`

### crouch_idle_right_to_crouch_idle_R_002__A245
- 说明：A person in a crouched position with their right leg forward steps it back while remaining in a crouched position.
- 名称：crouch_idle_right_to_crouch_idle_R；时长 3.62s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_idle_right_to_crouch_idle_R_002__A245.csv`

### crouch_idle_right_R_jogging_ff_start_225_R_walk_arc_cw_start_R_005__A472
- 说明：A person in a crouching position jogs forward towards the right diagonal, then slows down and starts walking in a clockwise direction.
- 名称：crouch_idle_right_R_jogging_ff_start_225_R_walk_arc_cw_start_R；时长 9.41s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231010/crouch_idle_right_R_jogging_ff_start_225_R_walk_arc_cw_start_R_005__A472.csv`

### crouch_operating_cupboard_low_out_R_002__A290
- 说明：A person with a crouched stance opens the cupboard and picks up an object from inside and then stands idle.
- 名称：crouch_operating_cupboard_low_out_R；时长 6.10s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230320/crouch_operating_cupboard_low_out_R_002__A290.csv`

### Relaxed_stoop_down_001__A057
- 说明：A person walking forward, relaxed and calm, leans down to pick up an object from the ground.
- 名称：relaxed_stoop_down_R；时长 10.62s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾
- CSV：`curated_600/motions/g1/csv/211117/Relaxed_stoop_down_001__A057.csv`

### crouch_cupboard_low_out_mid_loot_R_001__A289
- 说明：A person is looting a cupboard in a crouched position.
- 名称：crouch_cupboard_low_out_mid_loot_R；时长 12.02s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230320/crouch_cupboard_low_out_mid_loot_R_001__A289.csv`

### turn_crouch_270_R_003__A197
- 说明：A person standing in a crouching position while leaning forward quickly turns to their right and stands still, maintaining the same position.
- 名称：crouch_turn_270_R；时长 3.69s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/turn_crouch_270_R_003__A197.csv`

### squat_001__A362
- 说明：A person squats three times, then stands idle in an upright posture, facing forward.
- 名称：squat；时长 9.88s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230509/squat_001__A362.csv`

### idle_crouch_loop_003__A195
- 说明：A person is in a crouched position while facing forward.
- 名称：crouch_idle；时长 9.37s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/idle_crouch_loop_003__A195.csv`

### crouch_operating_cupboard_mid_out_R_003__A290
- 说明：A person extends and retracts their hands thrice while maintaining the crouched posture.
- 名称：crouch_operating_cupboard_mid_out_R；时长 5.21s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230320/crouch_operating_cupboard_mid_out_R_003__A290.csv`

### crouch_turn_360_R_001__A246
- 说明：A person turns back over the right shoulder in a couching stance.
- 名称：crouch_turn_360_R；时长 4.77s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_turn_360_R_001__A246.csv`

### crouch_ff_start_180_R_001__A247
- 说明：A crouched person starts to walk forward at a slow pace.
- 名称：crouch_ff_start_180_R；时长 5.72s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_ff_start_180_R_001__A247.csv`

### crouch_ff_stop_360_R_003__A247
- 说明：The person in a crouched stance moves backward while facing forward.
- 名称：crouch_ff_stop_360_R；时长 7.68s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_ff_stop_360_R_003__A247.csv`

### crouch_ff_stop_225_R_003__A198
- 说明：A person in a crouch position walks diagonally towards the right, then stops and stands in a crouch position.
- 名称：crouch_ff_stop_225_R；时长 9.18s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_stop_225_R_003__A198.csv`

### crouch_ff_stop_315_R_002__A247
- 说明：A person in a crouched position moving sideways to the right back diagonal comes to a stop.
- 名称：crouch_ff_stop_315_R；时长 7.56s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_ff_stop_315_R_002__A247.csv`

### crouch_ff_start_270_R_003__A196
- 说明：A person crouch-walks in a cross-stepping manner. Then they gradually stand upright as they continue moving to the right.
- 名称：crouch_ff_start_270_R；时长 5.94s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_start_270_R_003__A196.csv`

### crouch_ff_start_315_002__A126
- 说明：A person facing forward crouches down and begins to walk backward diagonally to the right while remaining in a crouched position.
- 名称：crouch_ff_start_315_R；时长 7.72s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230119/crouch_ff_start_315_002__A126.csv`

### crouch_ff_start_360_R_002__A248
- 说明：A person is steadily walking backwards in a fully crouched position.
- 名称：crouch_ff_start_360_R；时长 5.62s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_ff_start_360_R_002__A248.csv`

### crouch_ff_loop_225_R_003__A248
- 说明：A crouched person walks forward at a slow pace.
- 名称：crouch_ff_loop_225_R；时长 4.10s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_ff_loop_225_R_003__A248.csv`

### yawn_R_walk_ff_start_360_R_crouch_idle_R_002__A475
- 说明：A person standing raises their right arm, then walks backward, and then stands in a crouch stance.
- 名称：yawn_R_walk_ff_start_360_R_crouch_idle_R；时长 10.78s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231010/yawn_R_walk_ff_start_360_R_crouch_idle_R_002__A475.csv`

### crouch_walk_forward_and_back_turn_360_to_idle_R_002__A495
- 说明：A person standing bends to a crouched position and begins to walk forward, turning around and then returning to the starting point.
- 名称：crouch_walk_forward_and_back_turn_360_to_idle_R；时长 19.07s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：屈膝低姿态、躯干前倾、双手前伸
- CSV：`curated_600/motions/g1/csv/231024/crouch_walk_forward_and_back_turn_360_to_idle_R_002__A495.csv`

### Trusting_stoop_down_002__A057
- 说明：A person picks up an object from the ground while walking forward steadily.
- 名称：trusting_stoop_down；时长 6.30s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾
- CSV：`curated_600/motions/g1/csv/211117/Trusting_stoop_down_002__A057.csv`

### crouch_idle_right_to_crouch_idle_R_001__A246
- 说明：A person smoothly transitions from a low crouching stance with their right leg forward to a balanced crouching position, maintaining stability and control.
- 名称：crouch_idle_right_to_crouch_idle_R；时长 3.78s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_idle_right_to_crouch_idle_R_001__A246.csv`

### crouch_operating_cupboard_low_out_R_001__A288
- 说明：A person with a crouched stance opens the cupboard and picks up an object from inside and then stands idle.
- 名称：crouch_operating_cupboard_low_out_R；时长 6.52s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230320/crouch_operating_cupboard_low_out_R_001__A288.csv`

### crouch_ff_loop_360_R_003__A247
- 说明：A person with a slightly crouched stance walks backwards with heavy steps.
- 名称：crouch_ff_loop_360_R；时长 5.89s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_ff_loop_360_R_003__A247.csv`

### crouch_cupboard_low_out_mid_loot_R_003__A291
- 说明：A person standing upright bends down and opens a cupboard, picks up an object and places it above while in a crouched position.
- 名称：crouch_cupboard_low_out_mid_loot_R；时长 15.91s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230320/crouch_cupboard_low_out_mid_loot_R_003__A291.csv`

### Relaxed_stoop_down_004__A057
- 说明：A person walking forward, relaxed and calm, leans down to pick up an object from the ground.
- 名称：relaxed_stoop_down_R；时长 11.07s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾
- CSV：`curated_600/motions/g1/csv/211117/Relaxed_stoop_down_004__A057.csv`

### crouch_idle_to_crouch_idle_right_R_002__A248
- 说明：A person places the right leg forward while in a crouching position.
- 名称：crouch_idle_to_crouch_idle_right_R；时长 3.91s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_idle_to_crouch_idle_right_R_002__A248.csv`

### crouch_operating_cupboard_low_in_R_003__A297
- 说明：A person in a squatting position opens and closes a cupboard after placing an object inside.
- 名称：crouch_operating_cupboard_low_in_R；时长 5.01s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230322/crouch_operating_cupboard_low_in_R_003__A297.csv`

### crouch_cupboard_mid_out_R_002__A289
- 说明：A crouching person opens a cupboard, places an object inside, and then returns to their initial position.
- 名称：crouch_operating_cupboard_mid_out_R；时长 5.00s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230320/crouch_cupboard_mid_out_R_002__A289.csv`

### crouch_ff_loop_270_R_002__A196
- 说明：A person is stepping to their right in a crouching position while leaning forward slightly by taking quick steps.
- 名称：crouch_ff_loop_270_R；时长 5.68s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_loop_270_R_002__A196.csv`

### turn_crouch_360_R_003__A196
- 说明：A person turns back over the right shoulder in a couching stance.
- 名称：crouch_turn_360_R；时长 3.52s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/turn_crouch_360_R_003__A196.csv`

### item_pick_up_crouch_walk_R_002__A413
- 说明：A partially crouched person swiftly picks up an object from the floor with their right hand while walking forward.
- 名称：item_pick_up_crouch_walk_R；时长 3.85s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230530/item_pick_up_crouch_walk_R_002__A413.csv`

### crouch_ff_stop_360_R_003__A195
- 说明：The person in a crouched stance moves backward while facing forward.
- 名称：crouch_ff_stop_360_R；时长 7.01s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_stop_360_R_003__A195.csv`

### squat_002__A362
- 说明：A person squats three times, then stands idle in an upright posture, facing forward.
- 名称：squat；时长 7.49s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230509/squat_002__A362.csv`

### crouch_ff_stop_315_R_001__A196
- 说明：A person in a crouched position moving sideways to the right back diagonal comes to a stop.
- 名称：crouch_ff_stop_315_R；时长 6.17s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_stop_315_R_001__A196.csv`

### crouch_ff_loop_315_R_002__A197
- 说明：A crouched person walks sideways one step at a time to the right.
- 名称：crouch_ff_loop_315_R；时长 3.79s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_loop_315_R_002__A197.csv`

### crouch_ff_start_360_R_002__A197
- 说明：A person standing in a crouched stance walks backward at a normal speed.
- 名称：crouch_ff_start_360_R；时长 3.54s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_start_360_R_002__A197.csv`

### crouch_ff_loop_225_R_002__A197
- 说明：A crouched person walks forward at a slow pace.
- 名称：crouch_ff_loop_225_R；时长 3.93s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_loop_225_R_002__A197.csv`

### crouch_idle_right_to_crouch_idle_R_002__A247
- 说明：A person smoothly transitions from a low crouching stance with their right leg forward to a balanced crouching position, maintaining stability and control.
- 名称：crouch_idle_right_to_crouch_idle_R；时长 3.62s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_idle_right_to_crouch_idle_R_002__A247.csv`

### crouch_ff_loop_360_R_003__A197
- 说明：A person with a slightly crouched stance walks backwards with heavy steps.
- 名称：crouch_ff_loop_360_R；时长 4.65s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_loop_360_R_003__A197.csv`

### Trusting_stoop_down_001__A057
- 说明：A person walks forward, stops to bend down and pick up an object, then resumes walking and stops again.
- 名称：trusting_stoop_down；时长 11.04s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾
- CSV：`curated_600/motions/g1/csv/211117/Trusting_stoop_down_001__A057.csv`

### neutral_stoop_down_R_002__A075
- 说明：A person walks forward, leans down to pick up an object with their right hand, and then stands upright while facing forward.
- 名称：stoop_down_R；时长 6.25s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：屈膝低姿态、躯干前倾
- CSV：`curated_600/motions/g1/csv/221128/neutral_stoop_down_R_002__A075.csv`

### neutral_stoop_down_R_001__A123
- 说明：A person walks forward, leans down to pick up an object with their right hand, and then stands upright while facing forward.
- 名称：stoop_down_R；时长 7.59s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾
- CSV：`curated_600/motions/g1/csv/230118/neutral_stoop_down_R_001__A123.csv`

### idle_crouch_to_idle_crouch_right_R_003__A197
- 说明：A person places the right leg forward while in a crouching position.
- 名称：crouch_idle_to_crouch_idle_right_R；时长 4.00s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/idle_crouch_to_idle_crouch_right_R_003__A197.csv`

### crouch_operating_cupboard_mid_out_R_002__A297
- 说明：A person extends and retracts their hands thrice while maintaining the crouched posture.
- 名称：crouch_operating_cupboard_mid_out_R；时长 4.54s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230322/crouch_operating_cupboard_mid_out_R_002__A297.csv`

### item_pick_up_crouch_idle_R_002__A549
- 说明：A person in a crouch position picks up an object placed on the ground with their right hand.
- 名称：item_pick_up_crouch_idle_R；时长 5.33s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/240918/item_pick_up_crouch_idle_R_002__A549.csv`

### crouch_turn_270_R_002__A247
- 说明：A person standing in a crouching position while leaning forward quickly turns to their right and stands still, maintaining the same position.
- 名称：crouch_turn_270_R；时长 3.40s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_turn_270_R_002__A247.csv`

### crouch_cupboard_mid_in_R_003__A289
- 说明：A person is putting something into the medium-height cupboard while crouching.
- 名称：crouch_operating_cupboard_mid_in_R；时长 6.99s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230320/crouch_cupboard_mid_in_R_003__A289.csv`

### crouch_operating_cupboard_mid_in_R_003__A298
- 说明：A person is putting objects into a cupboard present at the torso level in front of them while in the crouched position.
- 名称：crouch_operating_cupboard_mid_in_R；时长 5.64s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230322/crouch_operating_cupboard_mid_in_R_003__A298.csv`

### crouch_ff_stop_180_R_003__A247
- 说明：A crouched person walks forward and then stands for a while.
- 名称：crouch_ff_stop_180_R；时长 7.68s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_ff_stop_180_R_003__A247.csv`

### turn_crouch_360_R_003__A197
- 说明：A person turns back over the right shoulder in a couching stance.
- 名称：crouch_turn_360_R；时长 4.11s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/turn_crouch_360_R_003__A197.csv`

### crouch_ff_stop_360_R_003__A197
- 说明：The person in a crouched stance moves backward while facing forward.
- 名称：crouch_ff_stop_360_R；时长 7.01s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_stop_360_R_003__A197.csv`

### item_pick_up_crouch_walk_R_003__A352
- 说明：A crouched person picks up an item while walking, then continues walking forward, facing down with swaying arms.
- 名称：item_pick_up_crouch_walk_R；时长 4.35s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸
- CSV：`curated_600/motions/g1/csv/230425/item_pick_up_crouch_walk_R_003__A352.csv`

### Relaxed_stoop_down_003__A057
- 说明：A person is walking forward, stooping down to pick up an item lying on the ground, walking again, and stopping and standing.
- 名称：relaxed_stoop_down_R；时长 11.14s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾
- CSV：`curated_600/motions/g1/csv/211117/Relaxed_stoop_down_003__A057.csv`

### crouch_idle_004__A247
- 说明：A person stands in a crouched posture and then starts to rise up.
- 名称：crouch_idle；时长 8.12s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_idle_004__A247.csv`

### item_pick_up_crouch_walk_R_001__A351
- 说明：A partially crouched person swiftly picks up an object from the floor with their right hand while walking forward.
- 名称：item_pick_up_crouch_walk_R；时长 4.43s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230425/item_pick_up_crouch_walk_R_001__A351.csv`

### crouch_ff_loop_270_R_002__A248
- 说明：A crouched person slowly and unsteadily walks sideways to their right.
- 名称：crouch_ff_loop_270_R；时长 6.52s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_ff_loop_270_R_002__A248.csv`

### crouch_ff_loop_180_R_003__A197
- 说明：A person is crouching while walking forward.
- 名称：crouch_ff_loop_180_R；时长 5.78s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_loop_180_R_003__A197.csv`

### crouch_ff_loop_315_R_002__A196
- 说明：A crouched person walks sideways one step at a time to the right.
- 名称：crouch_ff_loop_315_R；时长 3.79s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_loop_315_R_002__A196.csv`

### crouch_ff_stop_315_R_002__A196
- 说明：A person in a crouched position moving sideways to the right back diagonal comes to a stop.
- 名称：crouch_ff_stop_315_R；时长 5.65s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_stop_315_R_002__A196.csv`

### crouch_ff_start_360_R_003__A198
- 说明：A person standing in a crouched stance walks backward at a normal speed.
- 名称：crouch_ff_start_360_R；时长 4.78s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_start_360_R_003__A198.csv`

### crouch_ff_start_315_R_002__A247
- 说明：A person crouched down starts walking to their right back diagonal direction.
- 名称：crouch_ff_start_315_R；时长 5.39s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_ff_start_315_R_002__A247.csv`

### crouch_ff_start_315_R_003__A245
- 说明：A person facing forward crouches down and begins to walk backward diagonally to the right while remaining in a crouched position.
- 名称：crouch_ff_start_315_R；时长 6.03s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_ff_start_315_R_003__A245.csv`

### crouch_ff_start_270_R_001__A198
- 说明：A person crouch-walks in a cross-stepping manner. Then they gradually stand upright as they continue moving to the right.
- 名称：crouch_ff_start_270_R；时长 7.16s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_start_270_R_001__A198.csv`

### crouch_ff_stop_225_R_006__A196
- 说明：A person in a crouch position walks diagonally towards the right, then stops and stands in a crouch position.
- 名称：crouch_ff_stop_225_R；时长 6.72s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_stop_225_R_006__A196.csv`

### crouch_ff_stop_270_R_003__A197
- 说明：A person walks sideways to the right in a crouched posture, coordinating arm and leg movements, and gradually comes to a stop.
- 名称：crouch_ff_stop_270_R；时长 7.72s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_stop_270_R_003__A197.csv`

### crouch_ff_loop_225_R_003__A247
- 说明：A crouched person walks forward at a slow pace.
- 名称：crouch_ff_loop_225_R；时长 4.10s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_ff_loop_225_R_003__A247.csv`

### crouch_ff_start_360_R_003__A195
- 说明：A person standing in a crouched stance walks backward at a normal speed.
- 名称：crouch_ff_start_360_R；时长 4.47s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_start_360_R_003__A195.csv`

### crouch_ff_start_225_R_003__A248
- 说明：A person steadily walks while crouched in the right diagonal direction.
- 名称：crouch_ff_start_225_R；时长 5.71s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_ff_start_225_R_003__A248.csv`

### crouch_ff_start_225_R_001__A529
- 说明：A person steadily walks while crouched in the right diagonal direction.
- 名称：crouch_ff_start_225_R；时长 6.35s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231121/crouch_ff_start_225_R_001__A529.csv`

### crouch_operating_cupboard_low_out_R_001__A298
- 说明：A person with a crouched stance opens the cupboard and picks up an object from inside and then stands idle.
- 名称：crouch_operating_cupboard_low_out_R；时长 6.43s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230322/crouch_operating_cupboard_low_out_R_001__A298.csv`

### idle_crouch_right_to_idle_crouch_R_004__A197
- 说明：A person smoothly transitions from a low crouching stance with their right leg forward to a balanced crouching position, maintaining stability and control.
- 名称：crouch_idle_right_to_crouch_idle_R；时长 5.83s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/idle_crouch_right_to_idle_crouch_R_004__A197.csv`

### crouch_operating_cupboard_low_out_R_001__A290
- 说明：A person with a crouched stance opens the cupboard and picks up an object from inside and then stands idle.
- 名称：crouch_operating_cupboard_low_out_R；时长 4.97s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230320/crouch_operating_cupboard_low_out_R_001__A290.csv`

### crouch_ff_loop_360_R_002__A197
- 说明：A person with a slightly crouched stance walks backwards with heavy steps.
- 名称：crouch_ff_loop_360_R；时长 6.25s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_loop_360_R_002__A197.csv`

### neutral_stoop_down_R_003__A121
- 说明：A person walks forward, leans down to pick up an object with their right hand, and then stands upright while facing forward.
- 名称：stoop_down_R；时长 5.83s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态
- CSV：`curated_600/motions/g1/csv/230118/neutral_stoop_down_R_003__A121.csv`

### item_pick_up_crouch_idle_R_001__A352
- 说明：A person in a crouch position picks up an object placed on the ground with their right hand.
- 名称：item_pick_up_crouch_idle_R；时长 4.20s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230425/item_pick_up_crouch_idle_R_001__A352.csv`

### crouch_cupboard_low_out_mid_loot_R_003__A299
- 说明：A person in a crouched stance opens the cupboard door with right hand, picks up an item with left hand from a low shelf, places it on the middle shelf, sways their left hand sideways inside the cupboard, then closes the door.
- 名称：crouch_cupboard_low_out_mid_loot_R；时长 11.47s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230322/crouch_cupboard_low_out_mid_loot_R_003__A299.csv`

### crouch_operating_cupboard_mid_in_R_005__A298
- 说明：A person is putting objects into a cupboard present at the torso level in front of them while in the crouched position.
- 名称：crouch_operating_cupboard_mid_in_R；时长 5.09s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230322/crouch_operating_cupboard_mid_in_R_005__A298.csv`

### crouch_operating_cupboard_low_in_R_003__A298
- 说明：A person in a crouched position puts something in a cupboard with both their hands, then stands idle.
- 名称：crouch_operating_cupboard_low_in_R；时长 3.55s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230322/crouch_operating_cupboard_low_in_R_003__A298.csv`

### crouch_operating_cupboard_low_in_R_004__A299
- 说明：A person in a squatting position opens and closes a cupboard after placing an object inside.
- 名称：crouch_operating_cupboard_low_in_R；时长 6.49s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230322/crouch_operating_cupboard_low_in_R_004__A299.csv`

### idle_crouch_loop_001__A197
- 说明：A crouched person is standing in place and subtly swaying.
- 名称：crouch_idle；时长 9.62s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/idle_crouch_loop_001__A197.csv`

### crouch_ff_stop_180_R_001__A197
- 说明：A crouched person walks forward and then stands for a while.
- 名称：crouch_ff_stop_180_R；时长 9.14s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_stop_180_R_001__A197.csv`

### crouch_ff_loop_180_R_103__A125
- 说明：A person maintains a crouched posture and walks slowly and steadily while facing forward.
- 名称：crouch_ff_loop_180_R；时长 5.69s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230119/crouch_ff_loop_180_R_103__A125.csv`

### crouch_ff_stop_180_R_001__A198
- 说明：A person with a crouched stance walks forward and slowly comes to a halt.
- 名称：crouch_ff_stop_180_R；时长 6.84s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_stop_180_R_001__A198.csv`

### crouch_ff_loop_270_R_002__A247
- 说明：A crouched person walks sideways to their right at a steady pace.
- 名称：crouch_ff_loop_270_R；时长 6.52s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_ff_loop_270_R_002__A247.csv`

### crouch_ff_loop_315_R_002__A247
- 说明：A person in a crouched position is walking diagonally backward to their right.
- 名称：crouch_ff_loop_315_R；时长 4.52s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_ff_loop_315_R_002__A247.csv`

### item_pick_up_crouch_walk_R_003__A414
- 说明：A crouched person picks up an item while walking, then continues walking forward, facing down with swaying arms.
- 名称：item_pick_up_crouch_walk_R；时长 3.39s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230530/item_pick_up_crouch_walk_R_003__A414.csv`

### crouch_ff_start_270_R_001__A247
- 说明：A person crouch-walks in a cross-stepping manner. Then they gradually stand upright as they continue moving to the right.
- 名称：crouch_ff_start_270_R；时长 6.40s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_ff_start_270_R_001__A247.csv`

### crouch_ff_stop_270_R_002__A196
- 说明：A person walks sideways to the right in a crouched posture, coordinating arm and leg movements, and gradually comes to a stop.
- 名称：crouch_ff_stop_270_R；时长 5.87s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230215/crouch_ff_stop_270_R_002__A196.csv`

### crouch_ff_start_180_R_002__A245
- 说明：A person is steadily moving forward in a crouching position.
- 名称：crouch_ff_start_180_R；时长 5.63s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230306/crouch_ff_start_180_R_002__A245.csv`

## 弯腰避让：5 条

### neutral_avoid_obstacle_bend_down_jog_ff_180_R_001__A544
- 说明：A person avoids an obstacle while jogging forward steadily, then stands facing forward.
- 名称：neutral_avoid_obstacle_bend_down_jog_ff_180_R；时长 5.53s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：屈膝低姿态、躯干前倾、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/240529/neutral_avoid_obstacle_bend_down_jog_ff_180_R_001__A544.csv`

### neutral_avoid_obstacle_bend_down_walk_ff_180_R_001__A543
- 说明：A person bends and moves from under an obstacle to avoid it, walks forward, then stops.
- 名称：neutral_avoid_obstacle_bend_down_walk_ff_180_R；时长 9.31s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：躯干前倾
- CSV：`curated_600/motions/g1/csv/240529/neutral_avoid_obstacle_bend_down_walk_ff_180_R_001__A543.csv`

### neutral_avoid_obstacle_bend_down_walk_ff_180_R_001__A542
- 说明：A person bends forward to avoid an obstacle while walking, then straightens up and continues walking before coming to a stop.
- 名称：neutral_avoid_obstacle_bend_down_walk_ff_180_R；时长 6.49s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾
- CSV：`curated_600/motions/g1/csv/240529/neutral_avoid_obstacle_bend_down_walk_ff_180_R_001__A542.csv`

### neutral_avoid_obstacle_bend_down_jog_ff_180_R_001__A545
- 说明：A person quickly bends forward to avoid an obstacle, then jogs ahead and comes to a stop in an upright position.
- 名称：neutral_avoid_obstacle_bend_down_jog_ff_180_R；时长 6.06s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾
- CSV：`curated_600/motions/g1/csv/240529/neutral_avoid_obstacle_bend_down_jog_ff_180_R_001__A545.csv`

### neutral_avoid_obstacle_bend_down_jog_ff_180_R_001__A542
- 说明：A person quickly bends forward to avoid an obstacle, then jogs ahead and comes to a stop in an upright position.
- 名称：neutral_avoid_obstacle_bend_down_jog_ff_180_R；时长 4.29s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾
- CSV：`curated_600/motions/g1/csv/240529/neutral_avoid_obstacle_bend_down_jog_ff_180_R_001__A542.csv`

## 取物姿态：204 条

### medium_light_two_hands_pick_up_front_low_R_001__A506
- 说明：A person bends forward from an upright position, picks up a light object with both hands from the ground, and then stands straight while holding it.
- 名称：medium_light_two_hands_pick_up_front_low_R；时长 7.45s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231113/medium_light_two_hands_pick_up_front_low_R_001__A506.csv`

### medium_big_light_two_hands_pick_up_behind_low_R_001__A508
- 说明：The person turns back and lifts the object from the low behind and comes back to the normal stance while holding the object.
- 名称：medium_big_light_two_hands_pick_up_behind_low_R；时长 7.68s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_pick_up_behind_low_R_001__A508.csv`

### outside_door_knob_left_side_picklock_R_001__A513
- 说明：A person standing upright bends in a low, crouched position and attempts to pick the left-side door from outside with both hands.
- 名称：outside_door_knob_left_side_picklock_R；时长 7.98s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231115/outside_door_knob_left_side_picklock_R_001__A513.csv`

### big_light_two_hands_pick_up_right_side_medium_R_001__A511
- 说明：A person picks up an object from their right and faces forward, holding it at chest level.
- 名称：big_light_two_hands_pick_up_right_side_medium_R；时长 2.80s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_pick_up_right_side_medium_R_001__A511.csv`

### cigarette_pick_up_R_002__A458
- 说明：A person is smoking, holding a cigarette in their right hand. The cigarette drops to the ground, and they pick it up before continuing to smoke.
- 名称：cigarette_pick_up_R；时长 17.83s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：躯干前倾
- CSV：`curated_600/motions/g1/csv/231004/cigarette_pick_up_R_002__A458.csv`

### small_light_one_hand_pick_up_right_side_low_001__A507
- 说明：A person bends to the right side and picks up a small light object with the right hand.
- 名称：small_light_one_hand_pick_up_right_side_low_R；时长 3.73s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾
- CSV：`curated_600/motions/g1/csv/231113/small_light_one_hand_pick_up_right_side_low_001__A507.csv`

### small_light_two_hands_pick_up_front_high_R_001__A519
- 说明：A person standing upright picks up a small object with both hands from a high level and draws it closer to the chest.
- 名称：small_light_two_hands_pick_up_front_high_R；时长 3.27s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_two_hands_pick_up_front_high_R_001__A519.csv`

### small_light_two_hands_pick_up_right_side_low_R_001__A507
- 说明：A person is standing upright, bending to the right to pick up a low-height object with both hands, and then returning to an upright position while holding it.
- 名称：small_light_two_hands_pick_up_right_side_low_R；时长 2.96s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231113/small_light_two_hands_pick_up_right_side_low_R_001__A507.csv`

### big_light_one_hand_pick_up_front_high_R_001__A520
- 说明：The person picks up an object with their right hand from high up front.
- 名称：big_light_one_hand_pick_up_front_high_R；时长 4.63s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_one_hand_pick_up_front_high_R_001__A520.csv`

### medium_big_light_two_hands_pick_up_behind_high_R_002__A528
- 说明：A person picks up a big object from high up behind them and stands in place while holding it.
- 名称：medium_big_light_two_hands_pick_up_behind_high_R；时长 7.30s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231121/medium_big_light_two_hands_pick_up_behind_high_R_002__A528.csv`

### big_light_two_hands_pick_up_behind_low_R_001__A509
- 说明：A person picks up an object, and holds it in their arms as they stand idle.
- 名称：big_light_two_hands_pick_up_behind_low_R；时长 7.04s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_pick_up_behind_low_R_001__A509.csv`

### small_light_one_hand_pick_up_front_low_002__A506
- 说明：A person picks up a small object from a low position in front with their right hand and stands upright holding it.
- 名称：small_light_one_hand_pick_up_front_low_R；时长 7.20s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾
- CSV：`curated_600/motions/g1/csv/231113/small_light_one_hand_pick_up_front_low_002__A506.csv`

### pick_up_little_value_bill_R_003__A457
- 说明：A person picks up a bill from the ground, examines it by holding it upwards for a while, and then keeps it in the pocket.
- 名称：pick_up_little_value_bill_R；时长 9.93s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231004/pick_up_little_value_bill_R_003__A457.csv`

### medium_light_two_hands_pick_up_behind_medium_R_001__A510
- 说明：A person turns back and picks up a light object with both hands from a medium height. Then they turn to face forward.
- 名称：medium_light_two_hands_pick_up_behind_medium_R；时长 5.98s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_light_two_hands_pick_up_behind_medium_R_001__A510.csv`

### small_light_two_hands_pick_up_behind_low_R_002__A507
- 说明：A person crouches down to the right back diagonal to pick up an object from the low level before standing upright.
- 名称：small_light_two_hands_pick_up_behind_low_R；时长 3.51s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸
- CSV：`curated_600/motions/g1/csv/231113/small_light_two_hands_pick_up_behind_low_R_002__A507.csv`

### outside_door_knob_right_side_picklock_R_001__A515
- 说明：A person is taking a small step forward, bending down and picking a lock, and then taking a step backwards to stand upright.
- 名称：outside_door_knob_right_side_picklock_R；时长 6.45s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231115/outside_door_knob_right_side_picklock_R_001__A515.csv`

### big_light_one_hand_pick_up_right_side_low_R_002__A509
- 说明：A person turns to the right, picks up a large, lightweight object with their right hand, and extends their hands forward.
- 名称：big_light_one_hand_pick_up_right_side_low_R；时长 6.79s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_pick_up_right_side_low_R_002__A509.csv`

### medium_big_light_two_hands_pick_up_front_medium_R_001__A510
- 说明：A strong person leans forward to hold a light, medium-sized object, picks it up, gets in an upright position, and stands while holding it in an upright position.
- 名称：medium_big_light_two_hands_pick_up_front_medium_R；时长 7.80s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_pick_up_front_medium_R_001__A510.csv`

### item_pick_up_walk_R_003__A352
- 说明：A person walks forward with gentle arm swings, bends to pick up an item with their right hand, then straightens up and continues walking.
- 名称：item_pick_up_walk_R；时长 5.64s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸
- CSV：`curated_600/motions/g1/csv/230425/item_pick_up_walk_R_003__A352.csv`

### medium_light_two_hands_pick_up_right_side_high_R_001__A524
- 说明：A person picks up a medium-light object from a high position on the right and holds it in front.
- 名称：medium_light_two_hands_pick_up_right_side_high_R；时长 5.53s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_light_two_hands_pick_up_right_side_high_R_001__A524.csv`

### big_light_two_hands_put_down_front_high_R_001__A521
- 说明：A person extends both arms forward to pick an object from a height and hold it in front of them.
- 名称：big_light_two_hands_pick_up_front_high_R；时长 4.22s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_two_hands_put_down_front_high_R_001__A521.csv`

### medium_big_light_one_hand_pick_up_front_high_R_002__A526
- 说明：A person picks up a medium-sized light object with their right hand from high up in front.
- 名称：medium_big_light_one_hand_pick_up_front_high_R；时长 3.57s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_big_light_one_hand_pick_up_front_high_R_002__A526.csv`

### medium_big_light_one_hand_pick_up_behind_low_R_001__A507
- 说明：A person stands upright, turns right to grab an object at thigh level to their back with the right hand, and holds it forward at torso level.
- 名称：medium_big_light_one_hand_pick_up_behind_low_R；时长 3.31s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231113/medium_big_light_one_hand_pick_up_behind_low_R_001__A507.csv`

### medium_big_light_two_hands_pick_up_front_low_R_002__A508
- 说明：A person picks up an object from the ground and stands forward-facing while holding it near their chest.
- 名称：medium_big_light_two_hands_pick_up_front_low_R；时长 5.90s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_pick_up_front_low_R_002__A508.csv`

### pick_up_big_value_bill_R_001__A458
- 说明：A person bends to pick up a high-value bill. They then lift and inspects it, then lowers it and slips it near their right thigh.
- 名称：pick_up_big_value_bill_R；时长 16.29s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231004/pick_up_big_value_bill_R_001__A458.csv`

### small_light_one_hand_pick_up_behind_low_001__A505
- 说明：A person bends to their right, reaching behind them with their right hand to pick up an object. They then rise and turn to face forward while holding the object.
- 名称：small_light_one_hand_pick_up_behind_low_R；时长 6.58s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231113/small_light_one_hand_pick_up_behind_low_001__A505.csv`

### medium_big_light_one_hand_pick_up_front_low_R_003__A507
- 说明：A person bends forward to pick up a medium-sized, lightweight object with the right hand and places it at medium height.
- 名称：medium_big_light_one_hand_pick_up_front_low_R；时长 5.30s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸
- CSV：`curated_600/motions/g1/csv/231113/medium_big_light_one_hand_pick_up_front_low_R_003__A507.csv`

### medium_big_light_two_hands_pick_up_front_high_R_002__A531
- 说明：A person stands upright as they lift their arms to retrieve an object from a frontal elevated position and remains standing while holding the object and facing forward.
- 名称：medium_big_light_two_hands_pick_up_front_high_R；时长 7.25s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231121/medium_big_light_two_hands_pick_up_front_high_R_002__A531.csv`

### medium_big_light_two_hands_pick_up_behind_medium_R_001__A508
- 说明：A person is turning behind, picking up an object from a medium height and then again turning to face forward at a normal pace.
- 名称：medium_big_light_two_hands_pick_up_behind_medium_R；时长 4.24s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_pick_up_behind_medium_R_001__A508.csv`

### medium_light_two_hands_pick_up_front_medium_R_002__A510
- 说明：The person quickly picks up a medium-light object from mid-height in front and stands upright, holding it in front.
- 名称：medium_light_two_hands_pick_up_front_medium_R；时长 5.41s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_light_two_hands_pick_up_front_medium_R_002__A510.csv`

### medium_big_light_two_hands_pick_up_right_side_medium_R_001__A510
- 说明：A person standing upright turns to the right holds and lifts the object with both hands and turns to face forward.
- 名称：medium_big_light_two_hands_pick_up_right_side_medium_R；时长 3.67s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_pick_up_right_side_medium_R_001__A510.csv`

### small_light_one_hand_pick_up_behind_medium_R_001__A508
- 说明：A person turns forward after swiftly picking up a small, light object from medium height behind them with their right hand.
- 名称：small_light_one_hand_pick_up_behind_medium_R；时长 2.81s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/small_light_one_hand_pick_up_behind_medium_R_001__A508.csv`

### small_light_two_hands_pick_up_behind_medium_R_002__A508
- 说明：A person turns over the right shoulder while lifting their arms to pick an object with both hands from mid-behind before standing upright and facing forward.
- 名称：small_light_two_hands_pick_up_behind_medium_R；时长 3.92s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/231114/small_light_two_hands_pick_up_behind_medium_R_002__A508.csv`

### medium_light_two_hands_pick_up_behind_low_R_001__A506
- 说明：A person turns back to the right, picks up the object with both hands, then turns to the front and holds the object.
- 名称：medium_light_two_hands_pick_up_behind_low_R；时长 3.57s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231113/medium_light_two_hands_pick_up_behind_low_R_001__A506.csv`

### small_light_one_hand_pick_up_right_side_medium_R_002__A511
- 说明：A person picks up a small, light object with the right hand from the right side at medium height and holds it in front.
- 名称：small_light_one_hand_pick_up_right_side_medium_R；时长 4.62s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/small_light_one_hand_pick_up_right_side_medium_R_002__A511.csv`

### big_light_one_hand_pick_up_front_low_R_005__A511
- 说明：The person picks up a light object in front of them and then holds it in the front at the chest level.
- 名称：big_light_one_hand_pick_up_front_low_R；时长 7.58s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_pick_up_front_low_R_005__A511.csv`

### small_light_two_hands_pick_up_behind_high_R_001__A518
- 说明：A person turns back over their right shoulder to pick an object from the high shelf and then turns forward while holding the object.
- 名称：small_light_two_hands_pick_up_behind_high_R；时长 3.88s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_two_hands_pick_up_behind_high_R_001__A518.csv`

### big_light_one_hand_pick_up_right_side_medium_R_001__A511
- 说明：Standing erect, a person swiftly grabs an object from the right and moves it calmly at a medium level.
- 名称：big_light_one_hand_pick_up_right_side_medium_R；时长 4.17s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_pick_up_right_side_medium_R_001__A511.csv`

### medium_big_light_one_hand_pick_up_front_medium_R_003__A508
- 说明：A person picks up a medium-sized light object from a medium level in front and stands holding it.
- 名称：medium_big_light_one_hand_pick_up_front_medium_R；时长 6.33s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_one_hand_pick_up_front_medium_R_003__A508.csv`

### medium_light_two_hands_pick_up_right_side_medium_R_001__A511
- 说明：A person standing turns right, leans to pick up an object with both hands, then turns forward and stands while holding the object.
- 名称：medium_light_two_hands_pick_up_right_side_medium_R；时长 3.52s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_light_two_hands_pick_up_right_side_medium_R_001__A511.csv`

### big_light_two_hands_pick_up_right_side_high_R_001__A522
- 说明：A person picks up an object with both hands from a high position on the right side.
- 名称：big_light_two_hands_pick_up_right_side_high_R；时长 6.26s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_two_hands_pick_up_right_side_high_R_001__A522.csv`

### medium_light_two_hands_pick_up_behind_high_R_001__A524
- 说明：A person picks up an object from an elevated spot on their rear-right diagonal, lowers it while holding it, and turns to face forward.
- 名称：medium_light_two_hands_pick_up_behind_high_R；时长 3.77s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_light_two_hands_pick_up_behind_high_R_001__A524.csv`

### big_light_two_hands_pick_up_behind_medium_R_001__A511
- 说明：A person turns around and picks up a big, light object from a medium height.
- 名称：big_light_two_hands_pick_up_behind_medium_R；时长 3.42s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_pick_up_behind_medium_R_001__A511.csv`

### big_light_two_hands_pick_up_behind_high_R_001__A521
- 说明：A person turns around to pick up an object from a high point, then turns to face forward while holding the object.
- 名称：big_light_two_hands_pick_up_behind_high_R；时长 4.67s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_two_hands_pick_up_behind_high_R_001__A521.csv`

### medium_big_light_one_hand_pick_up_behind_high_R_001__A524
- 说明：A person steadily turns to the right, faces backwards, picks up an object from a high shelf, turns left, lowers their right arm in the front, and faces forward.
- 名称：medium_big_light_one_hand_pick_up_behind_high_R；时长 3.91s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_big_light_one_hand_pick_up_behind_high_R_001__A524.csv`

### big_light_one_hand_pick_up_front_medium_R_001__A511
- 说明：A person raises the right hand, picks up an object from the front of them, and then stands holding it in front of the torso.
- 名称：big_light_one_hand_pick_up_front_medium_R；时长 5.24s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_pick_up_front_medium_R_001__A511.csv`

### medium_big_light_one_hand_pick_up_behind_medium_R_001__A511
- 说明：The person reaches backward with their right hand to pick up a medium-big light object from medium height behind their body, then returns to an upright standing position with the object.
- 名称：medium_big_light_one_hand_pick_up_behind_medium_R；时长 3.31s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_one_hand_pick_up_behind_medium_R_001__A511.csv`

### medium_big_light_one_hand_pick_up_right_side_medium_R_001__A511
- 说明：A person picks up a light, medium-sized object using one hand from shoulder level on their right side.
- 名称：medium_big_light_one_hand_pick_up_right_side_medium_R；时长 6.20s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_one_hand_pick_up_right_side_medium_R_001__A511.csv`

### big_light_one_hand_pick_up_behind_low_R_002__A510
- 说明：A person swiftly turns backward to pick up an object, then turns forward while holding it.
- 名称：big_light_one_hand_pick_up_behind_low_R；时长 7.83s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_pick_up_behind_low_R_002__A510.csv`

### small_light_two_hands_pick_up_right_side_high_R_002__A516
- 说明：A person facing forward turns left, lifts their arms to the upper right to pick up an object, then turns back forward while lowering their arms.
- 名称：small_light_two_hands_pick_up_right_side_high_R；时长 3.07s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_two_hands_pick_up_right_side_high_R_002__A516.csv`

### small_light_one_hand_pick_up_behind_high_R_001__A519
- 说明：A person turns over the right shoulder to pick up a small, light object with the right hand from high up in front, then turns forward and stands.
- 名称：small_light_one_hand_pick_up_behind_high_R；时长 4.14s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231116/small_light_one_hand_pick_up_behind_high_R_001__A519.csv`

### item_pick_up_jog_R_003__A352
- 说明：A person jogs forward at a normal pace and quickly picks up an object from the ground with their right hand.
- 名称：item_pick_up_jog_R；时长 3.85s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾
- CSV：`curated_600/motions/g1/csv/230425/item_pick_up_jog_R_003__A352.csv`

### outside_door_handle_right_side_picklock_R_001__A508
- 说明：A person standing upright bends forward, attempting to pick a lock on a door.
- 名称：outside_door_handle_right_side_picklock_R；时长 9.23s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/outside_door_handle_right_side_picklock_R_001__A508.csv`

### big_light_two_hands_pick_up_right_side_low_R_001__A511
- 说明：A person bends down to their right to pick up an object and straightens up, coming to their initial position with the object in their hands.
- 名称：big_light_two_hands_pick_up_right_side_low_R；时长 3.52s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_pick_up_right_side_low_R_001__A511.csv`

### medium_big_light_one_hand_put_down_front_high_R_003__A524
- 说明：A person picks up a light object from high above to their right and holds it up in front of themselves using their right arm.
- 名称：medium_big_light_one_hand_pick_up_right_side_high_R；时长 5.42s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_big_light_one_hand_put_down_front_high_R_003__A524.csv`

### big_light_two_hands_pick_up_front_low_R_002__A508
- 说明：A person standing in an upright posture bends down, grasps an object from the ground, and raises it to neck level.
- 名称：big_light_two_hands_pick_up_front_low_R；时长 4.70s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_pick_up_front_low_R_002__A508.csv`

### item_pick_up_standing_R_004__A352
- 说明：A person quickly bends down to pick up an item and then stands upright while slightly swaying their arms.
- 名称：item_pick_up_standing_R；时长 5.25s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾
- CSV：`curated_600/motions/g1/csv/230425/item_pick_up_standing_R_004__A352.csv`

### pickaxe_digging_wall_R_003__A355
- 说明：A person holding a pickaxe is digging a wall in front of them.
- 名称：pickaxe_digging_wall_R；时长 14.93s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230427/pickaxe_digging_wall_R_003__A355.csv`

### pick_up_little_value_coin_R_001__A457
- 说明：A person bends forward and picks up a low-value coin from the ground with their right hand, then looks at the coin for a while before finally putting it into their right pocket.
- 名称：pick_up_little_value_coin_R；时长 9.95s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231004/pick_up_little_value_coin_R_001__A457.csv`

### small_light_two_hands_pick_up_front_low_R_001__A507
- 说明：A person bends down to quickly pick up an object from a low height, then straightens up while holding the object and stands upright.
- 名称：small_light_two_hands_pick_up_front_low_R；时长 3.80s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231113/small_light_two_hands_pick_up_front_low_R_001__A507.csv`

### pick_up_big_value_coin_R_002__A458
- 说明：A person bends down to pick up a high value coin, then observes it while holding it in one hand and later puts it in their pocket.
- 名称：pick_up_big_value_coin_R；时长 11.91s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸
- CSV：`curated_600/motions/g1/csv/231004/pick_up_big_value_coin_R_002__A458.csv`

### medium_big_light_two_hands_pick_up_right_side_low_R_001__A509
- 说明：A person standing gently bends down towards the right and picks up a medium-sized, big, light object placed on the floor on their right.
- 名称：medium_big_light_two_hands_pick_up_right_side_low_R；时长 4.58s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_pick_up_right_side_low_R_001__A509.csv`

### small_light_one_hand_pick_up_front_medium_R_001__A509
- 说明：The standing person extends the right arm and picks up the small, light object from medium height in front of the waist. Then, the person stands holding the object at mid-torso height.
- 名称：small_light_one_hand_pick_up_front_medium_R；时长 4.87s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/small_light_one_hand_pick_up_front_medium_R_001__A509.csv`

### small_light_one_hand_pick_up_behind_medium_R_001__A509
- 说明：A person picks up a small object with their right hand from medium a height behind them and stands upright holding it.
- 名称：small_light_one_hand_pick_up_behind_medium_R；时长 2.88s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/small_light_one_hand_pick_up_behind_medium_R_001__A509.csv`

### pick_up_little_value_bill_R_003__A458
- 说明：A person bends forward to pick up the bill, examines it, inserts it into their pocket, and lowers their arms to the side.
- 名称：pick_up_little_value_bill_R；时长 12.43s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231004/pick_up_little_value_bill_R_003__A458.csv`

### outside_door_knob_left_side_picklock_R_002__A513
- 说明：A person standing upright bends in a low, crouched position and attempts to pick the left-side door from outside with both hands.
- 名称：outside_door_knob_left_side_picklock_R；时长 7.89s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231115/outside_door_knob_left_side_picklock_R_002__A513.csv`

### small_light_two_hands_pick_up_right_side_medium_R_001__A511
- 说明：A person turns to the right, picks up an object from a medium height, then turns forward and stands, holding the object with both hands.
- 名称：small_light_two_hands_pick_up_right_side_medium_R；时长 6.16s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/small_light_two_hands_pick_up_right_side_medium_R_001__A511.csv`

### medium_big_light_one_hand_pick_up_right_side_low_R_001__A505
- 说明：A person slowly lifts an object from the right at thigh height with the right hand and then holds it forward.
- 名称：medium_big_light_one_hand_pick_up_right_side_low_R；时长 4.08s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾
- CSV：`curated_600/motions/g1/csv/231113/medium_big_light_one_hand_pick_up_right_side_low_R_001__A505.csv`

### medium_light_two_hands_pick_up_front_medium_R_002__A511
- 说明：A person stands upright, then swiftly extends their hands to pick up an object at waist level and bring it close to their chest.
- 名称：medium_light_two_hands_pick_up_front_medium_R；时长 5.41s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_light_two_hands_pick_up_front_medium_R_002__A511.csv`

### big_light_two_hands_pick_up_right_side_medium_R_001__A509
- 说明：A person picks up an object towards their right side and turns and stands idle while holding it.
- 名称：big_light_two_hands_pick_up_right_side_medium_R；时长 5.36s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_pick_up_right_side_medium_R_001__A509.csv`

### big_light_one_hand_pick_up_right_side_medium_R_001__A509
- 说明：The person picks up an object with their right hand and brings it forward at medium level.
- 名称：big_light_one_hand_pick_up_right_side_medium_R；时长 4.57s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_pick_up_right_side_medium_R_001__A509.csv`

### big_light_one_hand_pick_up_front_high_R_001__A523
- 说明：The person picks up an object with one hand from high up front.
- 名称：big_light_one_hand_pick_up_front_high_R；时长 4.29s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_one_hand_pick_up_front_high_R_001__A523.csv`

### medium_big_light_one_hand_pick_up_front_high_R_002__A525
- 说明：A person picks a medium big light object using right hand from a high height in front.
- 名称：medium_big_light_one_hand_pick_up_front_high_R；时长 3.67s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_big_light_one_hand_pick_up_front_high_R_002__A525.csv`

### medium_light_two_hands_pick_up_right_side_high_R_001__A525
- 说明：A person picks up a medium, light object from the high right side and holds it upright near chest level with both hands.
- 名称：medium_light_two_hands_pick_up_right_side_high_R；时长 5.03s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_light_two_hands_pick_up_right_side_high_R_001__A525.csv`

### medium_big_light_one_hand_pick_up_behind_low_R_001__A505
- 说明：A person steadily turns right to pick up an object from a lower shelf behind them using the right hand, then turns left and faces forward.
- 名称：medium_big_light_one_hand_pick_up_behind_low_R；时长 5.87s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231113/medium_big_light_one_hand_pick_up_behind_low_R_001__A505.csv`

### small_light_one_hand_pick_up_front_high_R_001__A519
- 说明：A person standing upright raises their right hand in front, picks up a small, light object from high up front, and lowers the object to their right.
- 名称：small_light_one_hand_pick_up_front_high_R；时长 2.43s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_one_hand_pick_up_front_high_R_001__A519.csv`

### medium_big_light_two_hands_pick_up_behind_medium_R_001__A510
- 说明：A person is turning behind, picking up an object from a medium height and then again turning to face forward at a normal pace.
- 名称：medium_big_light_two_hands_pick_up_behind_medium_R；时长 4.45s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_pick_up_behind_medium_R_001__A510.csv`

### big_light_two_hands_pick_up_behind_medium_R_001__A510
- 说明：A person turns back picks up an object with both hands from a medium height from behind and then turns forward.
- 名称：big_light_two_hands_pick_up_behind_medium_R；时长 3.12s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_pick_up_behind_medium_R_001__A510.csv`

### m_whaaat_grab_head_stadium_002__A041
- 说明：A person standing in a neutral position quickly holds their head with both hands and then raises their right hand closer to the face, lowers it, and stands still.
- 名称：whaaat_grab_head_stadium；时长 5.67s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/220728/m_whaaat_grab_head_stadium_002__A041.csv`

### medium_light_two_hands_pick_up_right_side_medium_R_001__A508
- 说明：A person standing still grabs an object located at waist height at their right side and holds it in front of the stomach.
- 名称：medium_light_two_hands_pick_up_right_side_medium_R；时长 5.74s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_light_two_hands_pick_up_right_side_medium_R_001__A508.csv`

### relax_grab_walk_ff_180_002__A552
- 说明：A person lowers their arms and walks forward with long strides at a moderated pace, picking up an object from the ground, then continues walking before standing in the initial position.
- 名称：relaxed_grab_walk_ff_180；时长 21.17s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/240918/relax_grab_walk_ff_180_002__A552.csv`

### big_light_one_hand_pick_up_behind_high_R_001__A520
- 说明：A person reaches up with their right hand to grab an object from a high position behind them.
- 名称：big_light_one_hand_pick_up_behind_high_R；时长 6.34s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_one_hand_pick_up_behind_high_R_001__A520.csv`

### medium_big_light_two_hands_pick_up_right_side_high_R_001__A531
- 说明：The person picks up an object using both their hands from their right side and places it forward at a medium level.
- 名称：medium_big_light_two_hands_pick_up_right_side_high_R；时长 7.35s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231121/medium_big_light_two_hands_pick_up_right_side_high_R_001__A531.csv`

### big_light_two_hands_put_down_front_high_R_001__A522
- 说明：A person picks up a big object from a high platform and lower it to their chest level.
- 名称：big_light_two_hands_pick_up_front_high_R；时长 2.92s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_two_hands_put_down_front_high_R_001__A522.csv`

### medium_light_two_hands_pick_up_behind_high_R_001__A526
- 说明：A person picks up a medium-light object from behind at a high level with both hands and brings it forward to hold in front.
- 名称：medium_light_two_hands_pick_up_behind_high_R；时长 5.80s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_light_two_hands_pick_up_behind_high_R_001__A526.csv`

### big_light_one_hand_pick_up_behind_low_R_002__A509
- 说明：A person picks up a light object from behind and then stands while raising their hand in the front.
- 名称：big_light_one_hand_pick_up_behind_low_R；时长 7.32s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_pick_up_behind_low_R_002__A509.csv`

### medium_light_two_hands_pick_up_behind_low_R_001__A507
- 说明：A person turns to the right and picks up a medium light object from a low position behind them using both hands.
- 名称：medium_light_two_hands_pick_up_behind_low_R；时长 4.92s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231113/medium_light_two_hands_pick_up_behind_low_R_001__A507.csv`

### big_light_two_hands_pick_up_right_side_low_R_001__A510
- 说明：A person standing upright, bends to the right, quickly grasps an object, briskly turns forward, and raises the object leisurely up with both hands.
- 名称：big_light_two_hands_pick_up_right_side_low_R；时长 3.80s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_pick_up_right_side_low_R_001__A510.csv`

### small_light_two_hands_pick_up_behind_medium_R_002__A510
- 说明：A person turns over the right shoulder while lifting their arms to pick an object with both hands from mid-behind before standing upright and facing forward.
- 名称：small_light_two_hands_pick_up_behind_medium_R；时长 3.08s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/231114/small_light_two_hands_pick_up_behind_medium_R_002__A510.csv`

### small_light_one_hand_pick_up_front_low_002__A507
- 说明：A person bends down and picks up a small object from the ground with their right hand before returning to stand upright.
- 名称：small_light_one_hand_pick_up_front_low_R；时长 7.20s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾
- CSV：`curated_600/motions/g1/csv/231113/small_light_one_hand_pick_up_front_low_002__A507.csv`

### medium_big_light_two_hands_pick_up_front_low_R_002__A509
- 说明：A person picks up an object from the ground and stands forward-facing while holding it near their chest.
- 名称：medium_big_light_two_hands_pick_up_front_low_R；时长 7.29s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_pick_up_front_low_R_002__A509.csv`

### medium_big_light_two_hands_pick_up_behind_high_R_002__A529
- 说明：A person picks up a big object from high up behind them and stands in place while holding it.
- 名称：medium_big_light_two_hands_pick_up_behind_high_R；时长 7.01s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231121/medium_big_light_two_hands_pick_up_behind_high_R_002__A529.csv`

### big_light_one_hand_pick_up_right_side_high_R_001__A521
- 说明：A person picks up a big, light object from a high level on their right side and holds it in the front at chest level.
- 名称：big_light_one_hand_pick_up_right_side_high_R；时长 6.70s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_one_hand_pick_up_right_side_high_R_001__A521.csv`

### big_light_one_hand_pick_up_behind_medium_R_001__A509
- 说明：A person picks up a light object from behind and turns forward while holding the object.
- 名称：big_light_one_hand_pick_up_behind_medium_R；时长 4.66s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_pick_up_behind_medium_R_001__A509.csv`

### pick_up_big_value_bill_R_001__A457
- 说明：A person bends down to pick up a high-value bill with their right hand, then stands upright and slips it into their right pocket, bouncing up and down with excitement.
- 名称：pick_up_big_value_bill_R；时长 14.85s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231004/pick_up_big_value_bill_R_001__A457.csv`

### small_light_one_hand_pick_up_right_side_low_001__A505
- 说明：The person picks up a small, light object with the right hand from a low height on the floor at the right side and then stands up straight.
- 名称：small_light_one_hand_pick_up_right_side_low_R；时长 3.86s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸
- CSV：`curated_600/motions/g1/csv/231113/small_light_one_hand_pick_up_right_side_low_001__A505.csv`

### small_light_two_hands_pick_up_front_high_R_001__A518
- 说明：The person quickly raises and extends both arms and grasp a small light object from high in front and lowers it.
- 名称：small_light_two_hands_pick_up_front_high_R；时长 1.99s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_two_hands_pick_up_front_high_R_001__A518.csv`

### big_light_two_hands_pick_up_behind_high_R_001__A522
- 说明：A person turns back, picks up a big object from a height, and holds it in front with both hands.
- 名称：big_light_two_hands_pick_up_behind_high_R；时长 4.21s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_two_hands_pick_up_behind_high_R_001__A522.csv`

### medium_big_light_one_hand_pick_up_behind_high_R_001__A527
- 说明：A person steadily turns to the right, faces backwards, picks up an object from a high shelf, turns left, lowers their right arm in the front, and faces forward.
- 名称：medium_big_light_one_hand_pick_up_behind_high_R；时长 4.58s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_big_light_one_hand_pick_up_behind_high_R_001__A527.csv`

### medium_big_light_one_hand_put_down_front_high_R_003__A526
- 说明：A person picks up a light object from high above to their right and holds it up in front of themselves using their right arm.
- 名称：medium_big_light_one_hand_pick_up_right_side_high_R；时长 4.80s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_big_light_one_hand_put_down_front_high_R_003__A526.csv`

### big_light_two_hands_pick_up_front_medium_R_001__A510
- 说明：A person picks up an object with both hands from the front and holds it while remaining still.
- 名称：big_light_two_hands_pick_up_front_medium_R；时长 5.15s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_pick_up_front_medium_R_001__A510.csv`

### small_light_two_hands_pick_up_behind_high_R_001__A517
- 说明：A person turns behind while raising their arms to pick an object with both hands from a high position and then turns around to face forward.
- 名称：small_light_two_hands_pick_up_behind_high_R；时长 2.71s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_two_hands_pick_up_behind_high_R_001__A517.csv`

### big_light_two_hands_pick_up_behind_low_R_001__A510
- 说明：A person turns back, picks up an object, and then faces forward.
- 名称：big_light_two_hands_pick_up_behind_low_R；时长 6.04s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_pick_up_behind_low_R_001__A510.csv`

### small_light_two_hands_pick_up_behind_low_R_002__A505
- 说明：A person picks up a small, light object from a low back shelf and stands while holding it in front of their torso with both hands.
- 名称：small_light_two_hands_pick_up_behind_low_R；时长 6.79s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231113/small_light_two_hands_pick_up_behind_low_R_002__A505.csv`

### medium_light_two_hands_pick_up_front_high_R_001__A524
- 说明：A person uses both hands to lift a medium-light object from high up front and holds it in front of their chest.
- 名称：medium_light_two_hands_pick_up_front_high_R；时长 3.96s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_light_two_hands_pick_up_front_high_R_001__A524.csv`

### grab_walk_ff_180_001__A552
- 说明：A person stands in a t-pose then lowers their arms and takes a step back then walks forward, later grab the object of the ground while walking, comes to a stop and stands in a t-pose.
- 名称：grab_walk_ff_180；时长 10.95s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：躯干前倾
- CSV：`curated_600/motions/g1/csv/240918/grab_walk_ff_180_001__A552.csv`

### small_light_two_hands_pick_up_right_side_high_R_002__A519
- 说明：A person turns right and raises their arm, picks up an object from the surface present to the right at their head level, and starts facing forward.
- 名称：small_light_two_hands_pick_up_right_side_high_R；时长 2.74s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_two_hands_pick_up_right_side_high_R_002__A519.csv`

### big_light_two_hands_pick_up_right_side_high_R_001__A520
- 说明：A person turns to their right and picks up an object from high up.
- 名称：big_light_two_hands_pick_up_right_side_high_R；时长 6.29s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_two_hands_pick_up_right_side_high_R_001__A520.csv`

### pickaxe_idle_R_002__A287
- 说明：A person stands still in an upright posture while firmly holding a pickaxe.
- 名称：pickaxe_idle_R；时长 15.70s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/230320/pickaxe_idle_R_002__A287.csv`

### medium_big_light_two_hands_pick_up_behind_low_R_001__A509
- 说明：A person standing upright picks up medium big light object with two hands from low height behind.
- 名称：medium_big_light_two_hands_pick_up_behind_low_R；时长 6.66s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_pick_up_behind_low_R_001__A509.csv`

### outside_door_handle_right_side_picklock_R_001__A510
- 说明：A person standing upright bends forward, attempting to pick a lock on a door.
- 名称：outside_door_handle_right_side_picklock_R；时长 6.93s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/outside_door_handle_right_side_picklock_R_001__A510.csv`

### item_pick_up_jog_R_001__A352
- 说明：A person jogs forward at a normal pace and quickly picks up an object from the ground with their right hand.
- 名称：item_pick_up_jog_R；时长 3.31s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾
- CSV：`curated_600/motions/g1/csv/230425/item_pick_up_jog_R_001__A352.csv`

### outside_door_knob_right_side_picklock_R_001__A512
- 说明：A person cautiously attempts to picklock a doorknob from outside by bending down forward.
- 名称：outside_door_knob_right_side_picklock_R；时长 5.19s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231115/outside_door_knob_right_side_picklock_R_001__A512.csv`

### big_light_two_hands_pick_up_front_low_R_002__A511
- 说明：A person standing in an upright posture bends down, grasps an object from the ground, and raises it to neck level.
- 名称：big_light_two_hands_pick_up_front_low_R；时长 3.24s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_pick_up_front_low_R_002__A511.csv`

### pick_up_little_value_coin_R_001__A458
- 说明：A person bends down and picks up a low-value coin and puts it into their pocket on the right side.
- 名称：pick_up_little_value_coin_R；时长 10.67s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231004/pick_up_little_value_coin_R_001__A458.csv`

### pick_up_big_value_coin_R_002__A457
- 说明：The person bends down, picks up a high-value coin with their right hand and then puts a coin in their pocket while standing upright.
- 名称：pick_up_big_value_coin_R；时长 12.47s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231004/pick_up_big_value_coin_R_002__A457.csv`

### pickaxe_digging_wall_R_006__A358
- 说明：A person holds a pickaxe in both hands, rapidly striking a wall in front of them.
- 名称：pickaxe_digging_wall_R；时长 12.68s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230427/pickaxe_digging_wall_R_006__A358.csv`

### small_light_two_hands_pick_up_front_low_R_001__A506
- 说明：A person picks up a small object with both hands from the ground while standing.
- 名称：small_light_two_hands_pick_up_front_low_R；时长 7.95s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231113/small_light_two_hands_pick_up_front_low_R_001__A506.csv`

### medium_big_light_two_hands_pick_up_right_side_low_R_001__A510
- 说明：A person is quickly bending to their right and picking up a heavy object before returning to a balanced stance while holding the object.
- 名称：medium_big_light_two_hands_pick_up_right_side_low_R；时长 8.12s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_pick_up_right_side_low_R_001__A510.csv`

### small_light_two_hands_pick_up_behind_medium_R_001__A511
- 说明：A person bends slightly to pick up a small, light object with both hands from medium height in front, then lifts it to chest level and stands upright.
- 名称：small_light_two_hands_pick_up_front_medium_R；时长 6.45s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/small_light_two_hands_pick_up_behind_medium_R_001__A511.csv`

### small_light_one_hand_pick_up_behind_medium_R_001__A510
- 说明：A person turns around and picks up a light object with the right hand from behind them and then turns to face forward.
- 名称：small_light_one_hand_pick_up_behind_medium_R；时长 3.83s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/small_light_one_hand_pick_up_behind_medium_R_001__A510.csv`

### big_light_one_hand_pick_up_front_medium_R_001__A508
- 说明：A person raises the right hand, picks up an object from the front of them, and then stands holding it in front of the torso.
- 名称：big_light_one_hand_pick_up_front_medium_R；时长 5.78s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_pick_up_front_medium_R_001__A508.csv`

### medium_light_two_hands_pick_up_behind_high_R_001__A527
- 说明：A person turns their torso over their right shoulder, picks up a medium-sized light object from behind with both hands, and turns back forward, holding it in front.
- 名称：medium_light_two_hands_pick_up_behind_high_R；时长 4.58s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_light_two_hands_pick_up_behind_high_R_001__A527.csv`

### m_whaaat_grab_head_stadium_003__A042
- 说明：A person standing in a neutral position quickly holds their head with both hands and then raises their right hand closer to the face, lowers it, and stands still.
- 名称：whaaat_grab_head_stadium；时长 6.85s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/220728/m_whaaat_grab_head_stadium_003__A042.csv`

### medium_big_light_two_hands_pick_up_right_side_high_R_001__A528
- 说明：A person picks up a medium, big, light object from the high right side and holds it at medium height in front of them.
- 名称：medium_big_light_two_hands_pick_up_right_side_high_R；时长 5.43s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231121/medium_big_light_two_hands_pick_up_right_side_high_R_001__A528.csv`

### walk_forward_grab_relax_001__A005
- 说明：A person stands in a t-pose lowers their arm and takes a step back and stands still, then walks forward in a relaxed state, later grabs the object off the ground while walking, comes to a stop and stands in a t-pose.
- 名称：relaxed_grab_walk_ff_180；时长 17.43s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/210707/walk_forward_grab_relax_001__A005.csv`

### small_light_two_hands_pick_up_behind_medium_R_002__A511
- 说明：A person turns their body backward, picks up a small light object using both their hands from a surface, having medium height, and then turns forward.
- 名称：small_light_two_hands_pick_up_behind_medium_R；时长 3.48s；保留该命名动作家族的典型版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/231114/small_light_two_hands_pick_up_behind_medium_R_002__A511.csv`

### small_light_one_hand_pick_up_behind_high_R_001__A518
- 说明：A person turns back over their right shoulder to pick up a small object from behind, then turns to the front while holding the object at torso level.
- 名称：small_light_one_hand_pick_up_behind_high_R；时长 3.90s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_one_hand_pick_up_behind_high_R_001__A518.csv`

### medium_big_light_two_hands_pick_up_behind_high_R_002__A531
- 说明：A person is turning over their right shoulder to pick up an object at a high level from behind, then turning to face forward and holding the object at waist level.
- 名称：medium_big_light_two_hands_pick_up_behind_high_R；时长 5.63s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231121/medium_big_light_two_hands_pick_up_behind_high_R_002__A531.csv`

### big_light_two_hands_put_down_front_high_R_001__A520
- 说明：A person extends both arms forward to pick an object from a height and hold it in front of them.
- 名称：big_light_two_hands_pick_up_front_high_R；时长 4.68s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_two_hands_put_down_front_high_R_001__A520.csv`

### big_light_two_hands_pick_up_right_side_medium_R_001__A510
- 说明：A person lifts an object from their right at medium height and holds it in front while standing.
- 名称：big_light_two_hands_pick_up_right_side_medium_R；时长 5.68s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_pick_up_right_side_medium_R_001__A510.csv`

### medium_big_light_one_hand_pick_up_right_side_medium_R_001__A508
- 说明：A person picks up a medium-sized light object with their right hand from their right side, lifts it, and then stands still while holding it.
- 名称：medium_big_light_one_hand_pick_up_right_side_medium_R；时长 2.66s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_one_hand_pick_up_right_side_medium_R_001__A508.csv`

### medium_big_light_two_hands_pick_up_behind_medium_R_001__A509
- 说明：The person picks up a big object by turning around over the right shoulder and returns back to face forward again while holding the object with both hands.
- 名称：medium_big_light_two_hands_pick_up_behind_medium_R；时长 4.25s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_pick_up_behind_medium_R_001__A509.csv`

### medium_big_light_two_hands_pick_up_front_medium_R_001__A511
- 说明：The person picks up a big object from the front at medium height using both hands and stands still, holding it steadily at torso level.
- 名称：medium_big_light_two_hands_pick_up_front_medium_R；时长 3.81s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_pick_up_front_medium_R_001__A511.csv`

### big_light_one_hand_pick_up_right_side_low_R_002__A508
- 说明：A person turns to the right, picks up a large, lightweight object with their right hand, and extends their hands forward.
- 名称：big_light_one_hand_pick_up_right_side_low_R；时长 5.68s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_pick_up_right_side_low_R_002__A508.csv`

### medium_big_light_one_hand_pick_up_behind_medium_R_001__A509
- 说明：A person swiftly lifts a big, light object from a medium height behind to the front with their right hand.
- 名称：medium_big_light_one_hand_pick_up_behind_medium_R；时长 3.59s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_one_hand_pick_up_behind_medium_R_001__A509.csv`

### big_light_two_hands_pick_up_front_medium_R_001__A508
- 说明：A person is facing and leaning forward to lift a big, lightweight object to a medium height with both hands while remaining stationary.
- 名称：big_light_two_hands_pick_up_front_medium_R；时长 5.49s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_pick_up_front_medium_R_001__A508.csv`

### medium_light_two_hands_pick_up_behind_medium_R_001__A511
- 说明：A person turns behind and bends down slightly to pick up a medium-light object with both hands, then turns back to face forward while holding the object.
- 名称：medium_light_two_hands_pick_up_behind_medium_R；时长 4.08s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_light_two_hands_pick_up_behind_medium_R_001__A511.csv`

### medium_big_light_one_hand_put_down_front_high_R_003__A527
- 说明：A person picks up a medium-sized light object from a high height with the right and holds it in front at shoulder level.
- 名称：medium_big_light_one_hand_pick_up_right_side_high_R；时长 5.09s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_big_light_one_hand_put_down_front_high_R_003__A527.csv`

### big_light_two_hands_pick_up_behind_high_R_001__A523
- 说明：A person turns backward to pick up an object with their hands from a high position behind them.
- 名称：big_light_two_hands_pick_up_behind_high_R；时长 4.38s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_two_hands_pick_up_behind_high_R_001__A523.csv`

### big_light_one_hand_pick_up_front_high_R_001__A521
- 说明：The person picks up an object with their right hand from high up front.
- 名称：big_light_one_hand_pick_up_front_high_R；时长 5.04s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_one_hand_pick_up_front_high_R_001__A521.csv`

### small_light_one_hand_pick_up_front_high_R_001__A517
- 说明：A person raises their right arm to pick up a small, light object, then retracts it and stands straight with the object in hand.
- 名称：small_light_one_hand_pick_up_front_high_R；时长 3.75s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_one_hand_pick_up_front_high_R_001__A517.csv`

### item_pick_up_walk_R_002__A413
- 说明：A person walks forward with gentle arm swings, bends to pick up an item with their right hand, then straightens up and continues walking.
- 名称：item_pick_up_walk_R；时长 4.89s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：屈膝低姿态、躯干前倾
- CSV：`curated_600/motions/g1/csv/230530/item_pick_up_walk_R_002__A413.csv`

### medium_big_light_two_hands_pick_up_front_high_R_002__A530
- 说明：The person picks up a light object placed high up front with both hands.
- 名称：medium_big_light_two_hands_pick_up_front_high_R；时长 6.49s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231121/medium_big_light_two_hands_pick_up_front_high_R_002__A530.csv`

### big_light_one_hand_pick_up_behind_medium_R_001__A508
- 说明：A person turns back, picks up an object placed in front of their shoulder, and brings it to the front.
- 名称：big_light_one_hand_pick_up_behind_medium_R；时长 3.03s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_pick_up_behind_medium_R_001__A508.csv`

### cigarette_pick_up_R_002__A456
- 说明：A person smoking a cigarette bends downward and picks up their cigarette, which falls on the ground, and puffs on it.
- 名称：cigarette_pick_up_R；时长 19.82s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231004/cigarette_pick_up_R_002__A456.csv`

### big_light_two_hands_pick_up_right_side_low_R_001__A508
- 说明：A person standing upright, bends to the right, quickly grasps an object, briskly turns forward, and raises the object leisurely up with both hands.
- 名称：big_light_two_hands_pick_up_right_side_low_R；时长 7.23s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_pick_up_right_side_low_R_001__A508.csv`

### walk_forward_grab_normal_001__A006
- 说明：A person standing in a t-pose lowers their arms and starts walking steadily, grabs something to the right on the ground with the right hand, then stops walking after some distance.
- 名称：grab_walk_ff_180；时长 15.44s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/210707/walk_forward_grab_normal_001__A006.csv`

### big_light_one_hand_pick_up_behind_high_R_001__A522
- 说明：A person reaches behind them and picks up a large, light object from a tall shelf above them.
- 名称：big_light_one_hand_pick_up_behind_high_R；时长 7.01s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_one_hand_pick_up_behind_high_R_001__A522.csv`

### small_light_one_hand_pick_up_behind_low_001__A506
- 说明：A standing person turns their torso over their right shoulder, bends down, and picks up a small, light object with one hand and then gets up.
- 名称：small_light_one_hand_pick_up_behind_low_R；时长 8.20s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾
- CSV：`curated_600/motions/g1/csv/231113/small_light_one_hand_pick_up_behind_low_001__A506.csv`

### small_light_two_hands_pick_up_behind_high_R_001__A516
- 说明：A person turns behind while raising their arms to pick an object with both hands from a high position and then turns around to face forward.
- 名称：small_light_two_hands_pick_up_behind_high_R；时长 2.57s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_two_hands_pick_up_behind_high_R_001__A516.csv`

### big_light_two_hands_pick_up_right_side_high_R_001__A523
- 说明：A person turns to the right, picks up an object from the top with both hands, then turns forward and stands while holding the object.
- 名称：big_light_two_hands_pick_up_right_side_high_R；时长 4.98s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_two_hands_pick_up_right_side_high_R_001__A523.csv`

### big_light_one_hand_pick_up_right_side_high_R_001__A523
- 说明：The person picks up an object from a higher level on their right and stands idle, holding the object in front of their waist.
- 名称：big_light_one_hand_pick_up_right_side_high_R；时长 7.52s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_one_hand_pick_up_right_side_high_R_001__A523.csv`

### item_pick_up_standing_R_003__A410
- 说明：A person quickly bends down and picks up an item from the ground with their right hand.
- 名称：item_pick_up_standing_R；时长 4.05s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸
- CSV：`curated_600/motions/g1/csv/230530/item_pick_up_standing_R_003__A410.csv`

### pickaxe_idle_R_101__A355
- 说明：A person is standing while holding a pickaxe.
- 名称：pickaxe_idle_R；时长 17.91s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/230427/pickaxe_idle_R_101__A355.csv`

### medium_light_two_hands_pick_up_front_high_R_001__A525
- 说明：A person reaches up in front with both hands to pick up a medium-light object and then stands upright holding the object.
- 名称：medium_light_two_hands_pick_up_front_high_R；时长 2.52s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_light_two_hands_pick_up_front_high_R_001__A525.csv`

### neutral_item_pick_up_table_R_001__A545
- 说明：A person swiftly raises their right hand forward at hip level to lift an object from the table and holds it at chest level.
- 名称：neutral_item_pick_up_table_R；时长 6.41s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/240529/neutral_item_pick_up_table_R_001__A545.csv`

### medium_big_light_two_hands_pick_up_right_side_medium_R_001__A508
- 说明：A person turns right from their waist, picks up a light-weight object by leaning forward, and then turns back to the normal position and then holds the object with both hands.
- 名称：medium_big_light_two_hands_pick_up_right_side_medium_R；时长 3.63s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_pick_up_right_side_medium_R_001__A508.csv`

### pick_up_big_value_bill_R_001__A459
- 说明：An enthusiastic person picks up a bill from the floor with both their hands, looks around and puts it in their right pocket.
- 名称：pick_up_big_value_bill_R；时长 13.45s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231004/pick_up_big_value_bill_R_001__A459.csv`

### pickaxe_digging_wall_R_004__A358
- 说明：A person holds a pickaxe in both hands, rapidly striking a wall in front of them.
- 名称：pickaxe_digging_wall_R；时长 12.86s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230427/pickaxe_digging_wall_R_004__A358.csv`

### small_light_two_hands_pick_up_behind_low_R_002__A506
- 说明：A person standing is turning to their right, bending down, and picking up a small, light object with both hands from a low height.
- 名称：small_light_two_hands_pick_up_behind_low_R；时长 3.69s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231113/small_light_two_hands_pick_up_behind_low_R_002__A506.csv`

### pick_up_little_value_bill_R_003__A459
- 说明：A person bends forward to pick up a low-value bill and puts it in their back pocket.
- 名称：pick_up_little_value_bill_R；时长 9.59s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231004/pick_up_little_value_bill_R_003__A459.csv`

### pick_up_big_value_coin_R_002__A456
- 说明：The person bends down, picks up a high-value coin with their right hand and then puts a coin in their pocket while standing upright.
- 名称：pick_up_big_value_coin_R；时长 13.12s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231004/pick_up_big_value_coin_R_002__A456.csv`

### pick_up_little_value_coin_R_001__A456
- 说明：A person bends forward and picks up a low-value coin from the ground with their right hand, then looks at the coin for a while before finally putting it into their right pocket.
- 名称：pick_up_little_value_coin_R；时长 14.03s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾
- CSV：`curated_600/motions/g1/csv/231004/pick_up_little_value_coin_R_001__A456.csv`

### big_light_two_hands_pick_up_front_low_R_002__A510
- 说明：A person bends and picks up an object.
- 名称：big_light_two_hands_pick_up_front_low_R；时长 7.91s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_pick_up_front_low_R_002__A510.csv`

### outside_door_knob_right_side_picklock_R_001__A513
- 说明：A person cautiously attempts to picklock a doorknob from outside by bending down forward.
- 名称：outside_door_knob_right_side_picklock_R；时长 6.81s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231115/outside_door_knob_right_side_picklock_R_001__A513.csv`

### medium_big_light_two_hands_pick_up_behind_low_R_001__A510
- 说明：The person turns back and lifts the object from the low behind and comes back to the normal stance while holding the object.
- 名称：medium_big_light_two_hands_pick_up_behind_low_R；时长 9.51s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_pick_up_behind_low_R_001__A510.csv`

### medium_light_two_hands_pick_up_behind_low_R_001__A505
- 说明：A person turns around behind them and picks up a medium-sized, light object from the ground with both hands before turning back to face forward.
- 名称：medium_light_two_hands_pick_up_behind_low_R；时长 6.97s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231113/medium_light_two_hands_pick_up_behind_low_R_001__A505.csv`

### medium_big_light_two_hands_pick_up_front_low_R_002__A510
- 说明：A person bends down to pick up a medium-sized, lightweight object from a low height with both hands, then stands in an upright stance holding the object in front of the torso.
- 名称：medium_big_light_two_hands_pick_up_front_low_R；时长 8.45s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_pick_up_front_low_R_002__A510.csv`

### medium_big_light_one_hand_pick_up_behind_low_R_001__A506
- 说明：A person is turning behind over their right shoulder, picking up an object from a lower height behind them and turning to face forward.
- 名称：medium_big_light_one_hand_pick_up_behind_low_R；时长 3.07s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾
- CSV：`curated_600/motions/g1/csv/231113/medium_big_light_one_hand_pick_up_behind_low_R_001__A506.csv`

### small_light_one_hand_pick_up_right_side_high_R_001__A516
- 说明：A person turns to steadily pick a small light object from the top right shelf with the right hand and then stands while holding it at the chest level.
- 名称：small_light_one_hand_pick_up_right_side_high_R；时长 2.92s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_one_hand_pick_up_right_side_high_R_001__A516.csv`

### small_light_one_hand_pick_up_behind_high_R_001__A516
- 说明：A person turns back to pick up a small, light object from high behind, and then they turn forward.
- 名称：small_light_one_hand_pick_up_behind_high_R；时长 3.20s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_one_hand_pick_up_behind_high_R_001__A516.csv`

### small_light_two_hands_pick_up_right_side_medium_R_001__A509
- 说明：A person picks up a small, light object with both hands from a medium height on their right side.
- 名称：small_light_two_hands_pick_up_right_side_medium_R；时长 3.21s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/small_light_two_hands_pick_up_right_side_medium_R_001__A509.csv`

### m_whaaat_grab_head_stadium_003__A043
- 说明：A person is standing in a relaxed posture, raises their arms and holds their head with both hands before dropping them.
- 名称：whaaat_grab_head_stadium；时长 6.00s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/220728/m_whaaat_grab_head_stadium_003__A043.csv`

### big_light_one_hand_pick_up_front_medium_R_001__A510
- 说明：A person picks up a light object from medium height up front and holds it at waist level.
- 名称：big_light_one_hand_pick_up_front_medium_R；时长 3.77s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_pick_up_front_medium_R_001__A510.csv`

### big_light_one_hand_pick_up_behind_low_R_002__A511
- 说明：A person picks up a light object from behind with the right hand and holds it forward.
- 名称：big_light_one_hand_pick_up_behind_low_R；时长 3.62s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_pick_up_behind_low_R_002__A511.csv`

### medium_light_two_hands_pick_up_right_side_medium_R_001__A509
- 说明：A person standing still grabs an object located at waist height at their right side and holds it in front of the stomach.
- 名称：medium_light_two_hands_pick_up_right_side_medium_R；时长 4.32s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_light_two_hands_pick_up_right_side_medium_R_001__A509.csv`

### relax_grab_walk_ff_180_001__A549
- 说明：A person lowers their arms and walks forward with long strides at a moderated pace, picking up an object from the ground, then continues walking before standing in the initial position.
- 名称：relaxed_grab_walk_ff_180；时长 18.93s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/240918/relax_grab_walk_ff_180_001__A549.csv`

### item_pick_up_walk_R_001__A350
- 说明：A person walking forward picks up an item from the ground with their right hand and continues walking at a steady pace.
- 名称：item_pick_up_walk_R；时长 5.77s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸
- CSV：`curated_600/motions/g1/csv/230425/item_pick_up_walk_R_001__A350.csv`

### small_light_two_hands_pick_up_right_side_high_R_002__A517
- 说明：A person swiftly turns to the right to pick up an object from an elevated platform using both hands, then turns back to face forward.
- 名称：small_light_two_hands_pick_up_right_side_high_R；时长 2.22s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_two_hands_pick_up_right_side_high_R_002__A517.csv`

### small_light_one_hand_pick_up_front_high_R_001__A516
- 说明：A person picks up a small, light object from a high position in front and brings it down near the body.
- 名称：small_light_one_hand_pick_up_front_high_R；时长 2.61s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_one_hand_pick_up_front_high_R_001__A516.csv`

### medium_big_light_two_hands_pick_up_front_high_R_002__A529
- 说明：A person raises their arms above their head to pick up a big, light objectfrom the higher front, and then they lower their arms to the chest level.
- 名称：medium_big_light_two_hands_pick_up_front_high_R；时长 8.82s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231121/medium_big_light_two_hands_pick_up_front_high_R_002__A529.csv`

### medium_big_light_one_hand_pick_up_behind_high_R_001__A525
- 说明：A person deliberately raises their right arm to pick up a big, light object from high behind and stands facing forward while holding it.
- 名称：medium_big_light_one_hand_pick_up_behind_high_R；时长 4.08s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_big_light_one_hand_pick_up_behind_high_R_001__A525.csv`

### medium_light_two_hands_pick_up_behind_medium_R_001__A509
- 说明：A person picks up an object placed behind them and holds it up.
- 名称：medium_light_two_hands_pick_up_behind_medium_R；时长 4.31s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_light_two_hands_pick_up_behind_medium_R_001__A509.csv`

### small_light_two_hands_pick_up_front_high_R_001__A516
- 说明：A person picks a light object from a high shelf with both hands.
- 名称：small_light_two_hands_pick_up_front_high_R；时长 1.96s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_two_hands_pick_up_front_high_R_001__A516.csv`

### medium_big_light_two_hands_pick_up_right_side_high_R_001__A530
- 说明：A person picks up an object from their right side and stands still, holding it in front of their torso with both hands.
- 名称：medium_big_light_two_hands_pick_up_right_side_high_R；时长 5.28s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231121/medium_big_light_two_hands_pick_up_right_side_high_R_001__A530.csv`

### small_light_two_hands_pick_up_behind_medium_R_001__A510
- 说明：The person picks up a small, light object using both hands from a medium-height position in front and continues to stand still holding it.
- 名称：small_light_two_hands_pick_up_front_medium_R；时长 5.06s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/small_light_two_hands_pick_up_behind_medium_R_001__A510.csv`

### medium_big_light_one_hand_pick_up_right_side_medium_R_001__A509
- 说明：A person turns right to pick up a big, light object with right hand, then faces forward holding it steadily.
- 名称：medium_big_light_one_hand_pick_up_right_side_medium_R；时长 5.33s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_one_hand_pick_up_right_side_medium_R_001__A509.csv`

### big_light_two_hands_pick_up_front_medium_R_001__A509
- 说明：A person picks up an object from a medium height with both hands from the front.
- 名称：big_light_two_hands_pick_up_front_medium_R；时长 3.38s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_pick_up_front_medium_R_001__A509.csv`

### medium_big_light_one_hand_pick_up_behind_medium_R_001__A510
- 说明：A person picks up a medium-sized, light object placed at a shoulder-level height behind them with their right hand.
- 名称：medium_big_light_one_hand_pick_up_behind_medium_R；时长 3.03s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_one_hand_pick_up_behind_medium_R_001__A510.csv`

### cigarette_pick_up_R_002__A457
- 说明：A person smoking a cigarette bends downward and picks up their cigarette, which falls on the ground, and puffs on it.
- 名称：cigarette_pick_up_R；时长 17.30s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231004/cigarette_pick_up_R_002__A457.csv`

### medium_big_light_one_hand_pick_up_front_medium_R_003__A509
- 说明：A person picks up a medium-sized light object with their right hand from a medium height in front.
- 名称：medium_big_light_one_hand_pick_up_front_medium_R；时长 3.92s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_one_hand_pick_up_front_medium_R_003__A509.csv`

### medium_big_light_two_hands_pick_up_front_medium_R_001__A508
- 说明：A strong person leans forward to hold a light, medium-sized object, picks it up, gets in an upright position, and stands while holding it in an upright position.
- 名称：medium_big_light_two_hands_pick_up_front_medium_R；时长 3.92s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_pick_up_front_medium_R_001__A508.csv`

### walk_forward_grab_normal_003__A417
- 说明：A person stands in a t-pose then lowers their arms and takes a step back then walks forward, later grab the object of the ground while walking, comes to a stop and stands in a t-pose.
- 名称：grab_walk_ff_180；时长 18.99s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/210707/walk_forward_grab_normal_003__A417.csv`

### item_pick_up_jog_R_001__A411
- 说明：A person picks up an item with the right hand while jogging steadily towards the right diagonal.
- 名称：item_pick_up_jog_R；时长 3.85s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾
- CSV：`curated_600/motions/g1/csv/230530/item_pick_up_jog_R_001__A411.csv`

### big_light_one_hand_pick_up_behind_medium_R_001__A510
- 说明：A person grabs an object from behind and then faces forward while holding it.
- 名称：big_light_one_hand_pick_up_behind_medium_R；时长 4.36s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_pick_up_behind_medium_R_001__A510.csv`

### big_light_one_hand_pick_up_behind_high_R_001__A521
- 说明：A person turns around to pick up an object behind them on a tall shelf with their right hand and puts it in front of them, facing forward.
- 名称：big_light_one_hand_pick_up_behind_high_R；时长 6.22s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_one_hand_pick_up_behind_high_R_001__A521.csv`

### item_pick_up_standing_R_003__A414
- 说明：A person quickly bends down to pick up an item and then stands upright while slightly swaying their arms.
- 名称：item_pick_up_standing_R；时长 6.83s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾
- CSV：`curated_600/motions/g1/csv/230530/item_pick_up_standing_R_003__A414.csv`

### big_light_one_hand_pick_up_right_side_high_R_001__A520
- 说明：A person picks up a big, light object from a high level on their right side and holds it in the front at chest level.
- 名称：big_light_one_hand_pick_up_right_side_high_R；时长 5.08s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_one_hand_pick_up_right_side_high_R_001__A520.csv`

### big_light_two_hands_pick_up_behind_medium_R_001__A508
- 说明：A person turns around and picks up a big, light object from a medium height.
- 名称：big_light_two_hands_pick_up_behind_medium_R；时长 3.19s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_pick_up_behind_medium_R_001__A508.csv`

### medium_light_two_hands_pick_up_right_side_high_R_001__A527
- 说明：A person picks up a medium-light object from a high position on the right and holds it in front.
- 名称：medium_light_two_hands_pick_up_right_side_high_R；时长 5.13s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_light_two_hands_pick_up_right_side_high_R_001__A527.csv`

### big_light_two_hands_pick_up_behind_low_R_001__A508
- 说明：A person turns back, picks up an object, and then faces forward.
- 名称：big_light_two_hands_pick_up_behind_low_R；时长 7.75s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_pick_up_behind_low_R_001__A508.csv`

### small_light_one_hand_pick_up_behind_low_001__A504
- 说明：A standing person turns their torso over their right shoulder, bends down, and picks up a small, light object with one hand and then gets up.
- 名称：small_light_one_hand_pick_up_behind_low_R；时长 4.61s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸
- CSV：`curated_600/motions/g1/csv/231113/small_light_one_hand_pick_up_behind_low_001__A504.csv`

### medium_big_light_two_hands_pick_up_right_side_medium_R_001__A509
- 说明：A person turns right from their waist, picks up a light-weight object by leaning forward, and then turns back to the normal position and then holds the object with both hands.
- 名称：medium_big_light_two_hands_pick_up_right_side_medium_R；时长 6.01s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_pick_up_right_side_medium_R_001__A509.csv`

## 放物姿态：141 条

### small_light_one_hand_put_down_front_low_001__A506
- 说明：The person standing, holding an object in the right hand, puts down the object on the ground and stands upright.
- 名称：small_light_one_hand_put_down_front_low_R；时长 6.95s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾
- CSV：`curated_600/motions/g1/csv/231113/small_light_one_hand_put_down_front_low_001__A506.csv`

### medium_light_two_hands_put_down_front_low_R_001__A505
- 说明：A person with a light object in their hands places it on the ground in front of them before standing up straight.
- 名称：medium_light_two_hands_put_down_front_low_R；时长 5.34s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231113/medium_light_two_hands_put_down_front_low_R_001__A505.csv`

### small_light_one_hand_put_down_behind_medium_R_001__A509
- 说明：A person carefully positions the light, small object behind them at a medium height in their right hand.
- 名称：small_light_one_hand_put_down_behind_medium_R；时长 3.80s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/small_light_one_hand_put_down_behind_medium_R_001__A509.csv`

### small_light_two_hands_put_down_front_high_R_001__A519
- 说明：A person swiftly places a small, light object in their hands at a high level in front.
- 名称：small_light_two_hands_put_down_front_high_R；时长 2.21s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_two_hands_put_down_front_high_R_001__A519.csv`

### big_light_two_hands_put_down_behind_low_R_001__A511
- 说明：A person turns to their right and places the big, lightweight object while holding it with both hands at a low height behind them.
- 名称：big_light_two_hands_put_down_behind_low_R；时长 5.95s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_put_down_behind_low_R_001__A511.csv`

### big_light_two_hands_put_down_right_side_medium_R_001__A511
- 说明：A person standing and holding an object with both hands places it to the right at the shoulder level, then turns to stand still.
- 名称：big_light_two_hands_put_down_right_side_medium_R；时长 4.80s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_put_down_right_side_medium_R_001__A511.csv`

### crutch_put_away_R_slow_003__A516
- 说明：A person holding a crutch in their right hand puts it away.
- 名称：crutch_put_away_R_slow；时长 13.32s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸
- CSV：`curated_600/motions/g1/csv/231116/crutch_put_away_R_slow_003__A516.csv`

### small_light_two_hands_put_down_front_low_R_001__A506
- 说明：A person holding a small, light object bends down to place it on the ground and then stands upright.
- 名称：small_light_two_hands_put_down_front_low_R；时长 2.94s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231113/small_light_two_hands_put_down_front_low_R_001__A506.csv`

### small_light_two_hands_put_down_front_medium_R_001__A511
- 说明：A person swiftly places a small, light object in their hands at a medium height in front while standing upright.
- 名称：small_light_two_hands_put_down_front_medium_R；时长 8.12s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/small_light_two_hands_put_down_front_medium_R_001__A511.csv`

### medium_big_light_two_hands_put_down_right_side_high_R_001__A528
- 说明：A standing person turns to their right, places an object on an elevated surface, and then lowers their arms and stands upright.
- 名称：medium_big_light_two_hands_put_down_right_side_high_R；时长 5.37s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231121/medium_big_light_two_hands_put_down_right_side_high_R_001__A528.csv`

### crutches_put_away_R_fast_002__A516
- 说明：A person standing puts the crutches away forward in the right diagonal direction.
- 名称：crutches_put_away_R_fast；时长 3.10s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/crutches_put_away_R_fast_002__A516.csv`

### big_light_one_hand_put_down_behind_high_R_001__A522
- 说明：A person turns backward, places an object above with the right hand, then turns forward and stands in an idle position.
- 名称：big_light_one_hand_put_down_behind_high_R；时长 6.24s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_one_hand_put_down_behind_high_R_001__A522.csv`

### medium_big_light_two_hands_put_down_right_side_low_R_002__A510
- 说明：A person holding a light, medium-sized object with two hands puts it down to their right before getting up and facing forward in an upright position.
- 名称：medium_big_light_two_hands_put_down_right_side_low_R；时长 9.02s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_put_down_right_side_low_R_002__A510.csv`

### big_light_two_hands_put_down_right_side_low_R_001__A509
- 说明：A person holding an object is placing it on the ground towards their right.
- 名称：big_light_two_hands_put_down_right_side_low_R；时长 4.55s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_put_down_right_side_low_R_001__A509.csv`

### crutches_put_away_R_001__A518
- 说明：An old person is putting away the crutches in the right diagonal and then stands upright.
- 名称：crutches_put_away_R；时长 8.57s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/crutches_put_away_R_001__A518.csv`

### small_light_one_hand_put_down_right_side_low_001__A507
- 说明：A standing person puts down a small object held in their right hand from medium level to low on the right side.
- 名称：small_light_one_hand_put_down_right_side_low_R；时长 7.34s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸
- CSV：`curated_600/motions/g1/csv/231113/small_light_one_hand_put_down_right_side_low_001__A507.csv`

### small_light_two_hands_put_down_behind_medium_R_001__A509
- 说明：A person puts a small, light object at a medium-level height behind them and stands upright facing forward.
- 名称：small_light_two_hands_put_down_behind_medium_R；时长 3.30s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/small_light_two_hands_put_down_behind_medium_R_001__A509.csv`

### medium_big_light_one_hand_put_down_right_side_low_R_001__A507
- 说明：A person puts an object in their right hand on the ground to their right and then stands upright.
- 名称：medium_big_light_one_hand_put_down_right_side_low_R；时长 3.19s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231113/medium_big_light_one_hand_put_down_right_side_low_R_001__A507.csv`

### medium_big_light_two_hands_put_down_right_side_medium_R_001__A510
- 说明：A person holds a big, light object, swiftly turns right to place it on a medium-height shelf.
- 名称：medium_big_light_two_hands_put_down_right_side_medium_R；时长 4.91s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_put_down_right_side_medium_R_001__A510.csv`

### small_light_two_hands_put_down_behind_low_R_001__A507
- 说明：A person swiftly turns around to face backward and bends down to place an object on the ground. They then stand upright and turn to face forward.
- 名称：small_light_two_hands_put_down_behind_low_R；时长 4.15s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸
- CSV：`curated_600/motions/g1/csv/231113/small_light_two_hands_put_down_behind_low_R_001__A507.csv`

### medium_big_light_one_hand_put_down_behind_low_R_001__A507
- 说明：A person picks up an object from behind and shifts their body to face forward.
- 名称：medium_big_light_one_hand_put_down_behind_low_R；时长 4.43s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231113/medium_big_light_one_hand_put_down_behind_low_R_001__A507.csv`

### big_light_one_hand_put_down_right_side_medium_R_001__A508
- 说明：A person holding an object in their right hand turns to the right and places it at shoulder level.
- 名称：big_light_one_hand_put_down_right_side_medium_R；时长 4.11s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_put_down_right_side_medium_R_001__A508.csv`

### big_light_two_hands_put_down_front_high_R_002__A521
- 说明：A person holding an object with both hands places it on a high platform above and stands straight.
- 名称：big_light_two_hands_put_down_front_high_R；时长 4.37s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_two_hands_put_down_front_high_R_002__A521.csv`

### medium_big_light_two_hands_put_down_behind_low_R_001__A508
- 说明：A person bends down at a right back diagonal to put an object with their hands and then stands while swaying their arms.
- 名称：medium_big_light_two_hands_put_down_behind_low_R；时长 6.84s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_put_down_behind_low_R_001__A508.csv`

### medium_big_light_two_hands_put_down_right_side_medium_R_002__A510
- 说明：A person standing, holding a large light object with both hands, turns around over their right shoulder and places it at the midsection behind them.
- 名称：medium_big_light_two_hands_put_down_behind_medium_R；时长 5.31s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_put_down_right_side_medium_R_002__A510.csv`

### small_light_one_hand_put_down_front_medium_R_001__A509
- 说明：A person holding an object in their right arm puts it down in front of them and then stands in an upright stance.
- 名称：small_light_one_hand_put_down_front_medium_R；时长 3.95s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/small_light_one_hand_put_down_front_medium_R_001__A509.csv`

### big_light_one_hand_put_down_front_low_R_002__A509
- 说明：The person puts down an object with their right hand.
- 名称：big_light_one_hand_put_down_front_low_R；时长 5.21s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_put_down_front_low_R_002__A509.csv`

### medium_big_light_one_hand_put_down_behind_medium_R_001__A509
- 说明：A person standing upright turns to their right, places the large object behind them, and then turns back to face forward.
- 名称：medium_big_light_one_hand_put_down_behind_medium_R；时长 6.12s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_one_hand_put_down_behind_medium_R_001__A509.csv`

### small_light_one_hand_put_down_right_side_high_R_001__A519
- 说明：A person standing puts the object to the right above the shoulder level, then turns back and stands still.
- 名称：small_light_one_hand_put_down_right_side_high_R；时长 3.05s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_one_hand_put_down_right_side_high_R_001__A519.csv`

### medium_big_light_one_hand_put_down_behind_high_R_001__A524
- 说明：A person lifts their right hand and places an object onto a raised platform behind them.
- 名称：medium_big_light_one_hand_put_down_behind_high_R；时长 4.43s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_big_light_one_hand_put_down_behind_high_R_001__A524.csv`

### medium_big_light_two_hands_put_down_front_medium_R_001__A509
- 说明：A person puts down big object with two hands at medium height up front.
- 名称：medium_big_light_two_hands_put_down_front_medium_R；时长 4.97s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_put_down_front_medium_R_001__A509.csv`

### small_light_two_hands_put_down_behind_high_R_001__A516
- 说明：A person holding small, light object in front swiftly turns behind to place it high up and then turns forward to stand relaxed.
- 名称：small_light_two_hands_put_down_behind_high_R；时长 2.79s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_two_hands_put_down_behind_high_R_001__A516.csv`

### small_light_one_hand_put_down_behind_high_R_002__A518
- 说明：A person holds a small, light object in their right hand and places it at a high level behind them.
- 名称：small_light_one_hand_put_down_behind_high_R；时长 4.19s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_one_hand_put_down_behind_high_R_002__A518.csv`

### medium_big_light_two_hands_put_down_behind_high_R_001__A531
- 说明：A person puts away a big object in their hands behind them, above head level, before standing still facing forward.
- 名称：medium_big_light_two_hands_put_down_behind_high_R；时长 6.65s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231121/medium_big_light_two_hands_put_down_behind_high_R_001__A531.csv`

### medium_light_two_hands_put_down_behind_medium_R_001__A509
- 说明：A person turns back while holding an object with both hands, puts it down at a medium height behind them, and then turns around.
- 名称：medium_light_two_hands_put_down_behind_medium_R；时长 6.95s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/medium_light_two_hands_put_down_behind_medium_R_001__A509.csv`

### medium_light_two_hands_put_down_behind_high_R_001__A525
- 说明：A person holding a medium-sized object with both hands turns to the right and places it high behind them, then returns to a posture with hands lowered at their sides.
- 名称：medium_light_two_hands_put_down_behind_high_R；时长 4.83s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_light_two_hands_put_down_behind_high_R_001__A525.csv`

### medium_light_two_hands_put_down_behind_low_R_001__A507
- 说明：A person holding an object in both hands turns backward and places the object on the ground.
- 名称：medium_light_two_hands_put_down_behind_low_R；时长 8.56s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231113/medium_light_two_hands_put_down_behind_low_R_001__A507.csv`

### medium_light_two_hands_put_down_front_medium_R_001__A511
- 说明：A person puts down an object held in their hands to their right side at medium height and stands upright.
- 名称：medium_light_two_hands_put_down_front_medium_R；时长 4.26s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_light_two_hands_put_down_front_medium_R_001__A511.csv`

### big_light_two_hands_put_down_behind_high_R_001__A521
- 说明：A person turns backward over the right side to place an object down with both hands at a high position.
- 名称：big_light_two_hands_put_down_behind_high_R；时长 6.10s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_two_hands_put_down_behind_high_R_001__A521.csv`

### big_light_two_hands_put_down_front_medium_R_001__A509
- 说明：A person holding an object puts it away in front at a medium height before standing still.
- 名称：big_light_two_hands_put_down_front_medium_R；时长 3.73s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_put_down_front_medium_R_001__A509.csv`

### medium_big_light_two_hands_put_down_front_low_R_001__A511
- 说明：A person bends down to put a big, light object on the ground and then they raise their body and stand.
- 名称：medium_big_light_two_hands_put_down_front_low_R；时长 4.53s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_put_down_front_low_R_001__A511.csv`

### big_light_one_hand_put_down_front_high_R_003__A523
- 说明：A person places an object at a high height in front of them and then stands idly.
- 名称：big_light_one_hand_put_down_front_high_R；时长 4.63s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_one_hand_put_down_front_high_R_003__A523.csv`

### medium_big_light_two_hands_put_down_front_high_R_001__A531
- 说明：A person holding an object in both hands places it in front above the head level before standing idle.
- 名称：medium_big_light_two_hands_put_down_front_high_R；时长 6.11s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231121/medium_big_light_two_hands_put_down_front_high_R_001__A531.csv`

### medium_light_two_hands_put_down_right_side_high_R_001__A524
- 说明：A person puts a big, light object on the upper right side, and then they lower their arms and turn forward.
- 名称：medium_light_two_hands_put_down_right_side_high_R；时长 4.62s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_light_two_hands_put_down_right_side_high_R_001__A524.csv`

### medium_big_light_one_hand_put_down_right_side_high_R_001__A525
- 说明：An upright person holding a big light object in their right hand slowly raises it and keeps it to the right at a high level.
- 名称：medium_big_light_one_hand_put_down_right_side_high_R；时长 5.36s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_big_light_one_hand_put_down_right_side_high_R_001__A525.csv`

### big_light_one_hand_put_down_behind_medium_R_003__A511
- 说明：A person lifting an object at a medium level turns around from the right, puts it down at the same level with one hand, and then turns forward.
- 名称：big_light_one_hand_put_down_behind_medium_R；时长 5.23s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_put_down_behind_medium_R_003__A511.csv`

### small_light_two_hands_put_down_right_side_high_R_001__A518
- 说明：A person holds a small, light object with both hands in front and puts it away on the high right side.
- 名称：small_light_two_hands_put_down_right_side_high_R；时长 2.52s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_two_hands_put_down_right_side_high_R_001__A518.csv`

### big_light_two_hands_put_down_right_side_high_R_001__A522
- 说明：A person holding an object turns to the right and places it in a high position before turning around to face forward.
- 名称：big_light_two_hands_put_down_right_side_high_R；时长 7.50s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_two_hands_put_down_right_side_high_R_001__A522.csv`

### big_light_one_hand_put_down_right_side_high_R_002__A522
- 说明：A person lifts their right arm while stepping right to put down a light object high at the right.
- 名称：big_light_one_hand_put_down_right_side_high_R；时长 5.66s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_one_hand_put_down_right_side_high_R_002__A522.csv`

### neutral_item_put_down_table_R_001__A545
- 说明：A person standing calmly while holding an item gently places it down on a table and then stands in an idle position.
- 名称：neutral_item_put_down_table_R；时长 2.23s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/240529/neutral_item_put_down_table_R_001__A545.csv`

### medium_big_light_one_hand_put_down_right_side_medium_R_001__A511
- 说明：A person steadily turns to the right and places an object on the right-side shelf.
- 名称：medium_big_light_one_hand_put_down_right_side_medium_R；时长 3.87s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_one_hand_put_down_right_side_medium_R_001__A511.csv`

### big_light_one_hand_put_down_behind_low_R_002__A511
- 说明：A person holding an object turns back and puts it behind them.
- 名称：big_light_one_hand_put_down_behind_low_R；时长 4.68s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_put_down_behind_low_R_002__A511.csv`

### big_light_two_hands_put_down_behind_medium_R_001__A508
- 说明：A person rotates 180 degrees in clockwise direction, puts down an object and then rotates in an anti-clockwise direction.
- 名称：big_light_two_hands_put_down_behind_medium_R；时长 4.70s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_put_down_behind_medium_R_001__A508.csv`

### small_light_two_hands_put_down_right_side_low_R_001__A506
- 说明：A person turns to the right while putting down a small light object with both hands.
- 名称：small_light_two_hands_put_down_right_side_low_R；时长 3.47s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231113/small_light_two_hands_put_down_right_side_low_R_001__A506.csv`

### big_light_one_hand_put_down_front_medium_R_002__A511
- 说明：A person holding an object in front of them with their right arm puts it on a platform slightly high above at the front medium level height.
- 名称：big_light_one_hand_put_down_front_medium_R；时长 3.34s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_put_down_front_medium_R_002__A511.csv`

### big_light_two_hands_put_down_front_low_R_001__A508
- 说明：The person places the object down with both hands at a low height in front of them.
- 名称：big_light_two_hands_put_down_front_low_R；时长 7.39s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_put_down_front_low_R_001__A508.csv`

### big_light_two_hands_put_down_right_side_low_R_001__A510
- 说明：A person is placing an object down at a low height to their right with their both hands.
- 名称：big_light_two_hands_put_down_right_side_low_R；时长 7.53s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_put_down_right_side_low_R_001__A510.csv`

### crutches_put_away_R_001__A516
- 说明：A person carefully puts down the crutches in the forward right diagonal and stands slightly unbalanced.
- 名称：crutches_put_away_R；时长 7.13s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/crutches_put_away_R_001__A516.csv`

### medium_big_light_one_hand_put_down_behind_low_R_001__A504
- 说明：A person holds an object with their right hand, then quickly turns right to place it behind them at hip level.
- 名称：medium_big_light_one_hand_put_down_behind_low_R；时长 4.01s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231113/medium_big_light_one_hand_put_down_behind_low_R_001__A504.csv`

### small_light_two_hands_put_down_behind_medium_R_001__A508
- 说明：A person holding a small light object in both hands turns back over the right shoulder to steadily place it on the medium back shelf.
- 名称：small_light_two_hands_put_down_behind_medium_R；时长 4.66s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/small_light_two_hands_put_down_behind_medium_R_001__A508.csv`

### crutch_put_away_R_slow_003__A518
- 说明：A person holding a crutch in their right hand puts it away.
- 名称：crutch_put_away_R_slow；时长 9.19s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾
- CSV：`curated_600/motions/g1/csv/231116/crutch_put_away_R_slow_003__A518.csv`

### small_light_two_hands_put_down_right_side_medium_R_001__A509
- 说明：A person turns and steadily places a small object on the medium right shelf. They then turn to face forward and lower their arms to stand upright.
- 名称：small_light_two_hands_put_down_right_side_medium_R；时长 3.33s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/small_light_two_hands_put_down_right_side_medium_R_001__A509.csv`

### medium_big_light_two_hands_put_down_right_side_medium_R_002__A508
- 说明：A person standing, holding a large light object with both hands, turns around over their right shoulder and places it at the midsection behind them.
- 名称：medium_big_light_two_hands_put_down_behind_medium_R；时长 6.56s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_put_down_right_side_medium_R_002__A508.csv`

### cellpone_put_away_stand_R_001__A427
- 说明：A person puts a cellphone in their pocket with their right hand and stands straight.
- 名称：cellphone_put_away_stand_R；时长 7.62s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/230711/cellpone_put_away_stand_R_001__A427.csv`

### big_light_one_hand_put_down_right_side_medium_R_001__A509
- 说明：A person holding an object in their right hand turns to the right and places it at shoulder level.
- 名称：big_light_one_hand_put_down_right_side_medium_R；时长 3.64s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_put_down_right_side_medium_R_001__A509.csv`

### medium_big_light_two_hands_put_down_front_low_R_001__A510
- 说明：A person standing still while holding an object with both hands bends forward and places the object on the ground in front.
- 名称：medium_big_light_two_hands_put_down_front_low_R；时长 8.55s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_put_down_front_low_R_001__A510.csv`

### big_light_two_hands_put_down_behind_low_R_001__A509
- 说明：A person standing, holding an object at shoulder level with both hands, turns, places it behind them, turns again, and then stands idle.
- 名称：big_light_two_hands_put_down_behind_low_R；时长 7.16s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_put_down_behind_low_R_001__A509.csv`

### medium_big_light_two_hands_put_down_right_side_medium_R_001__A511
- 说明：A person places a medium-sized light object on a medium-sized shelf with both hands.
- 名称：medium_big_light_two_hands_put_down_right_side_medium_R；时长 5.18s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_put_down_right_side_medium_R_001__A511.csv`

### small_light_one_hand_put_down_behind_high_R_002__A516
- 说明：A person holds a small, light object in their right hand and places it at a high level behind them.
- 名称：small_light_one_hand_put_down_behind_high_R；时长 3.41s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231116/small_light_one_hand_put_down_behind_high_R_002__A516.csv`

### medium_big_light_two_hands_put_down_behind_high_R_001__A528
- 说明：A person holding an object with both hands turns around over their right shoulder, places it on the top shelf, and then stands upright.
- 名称：medium_big_light_two_hands_put_down_behind_high_R；时长 6.92s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231121/medium_big_light_two_hands_put_down_behind_high_R_001__A528.csv`

### medium_big_light_one_hand_put_down_behind_high_R_001__A527
- 说明：A person holding an object turns to the right to place it using their right hand and drops their arm to face forward.
- 名称：medium_big_light_one_hand_put_down_behind_high_R；时长 4.92s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_big_light_one_hand_put_down_behind_high_R_001__A527.csv`

### small_light_two_hands_put_down_behind_high_R_001__A517
- 说明：A person holding small, light object in front swiftly turns behind to place it high up and then turns forward to stand relaxed.
- 名称：small_light_two_hands_put_down_behind_high_R；时长 2.69s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_two_hands_put_down_behind_high_R_001__A517.csv`

### big_light_two_hands_put_down_behind_high_R_001__A522
- 说明：A person places an object behind them and turns back to stand idle.
- 名称：big_light_two_hands_put_down_behind_high_R；时长 5.11s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_two_hands_put_down_behind_high_R_001__A522.csv`

### big_light_one_hand_put_down_front_high_R_002__A522
- 说明：A person puts down a big object with one hand from high upfront.
- 名称：big_light_one_hand_put_down_front_high_R；时长 5.75s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_one_hand_put_down_front_high_R_002__A522.csv`

### medium_big_light_two_hands_put_down_right_side_high_R_001__A531
- 说明：A person places an object on the high shelf.
- 名称：medium_big_light_two_hands_put_down_right_side_high_R；时长 5.67s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231121/medium_big_light_two_hands_put_down_right_side_high_R_001__A531.csv`

### medium_big_light_one_hand_put_down_front_high_R_002__A525
- 说明：A person places an object on a high platform towards their front with their right arm and then lowers their hand to stand straight.
- 名称：medium_big_light_one_hand_put_down_front_high_R；时长 5.16s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_big_light_one_hand_put_down_front_high_R_002__A525.csv`

### small_light_one_hand_put_down_right_side_high_R_001__A517
- 说明：A person holding an object in their right hand turns to the right to place it on an elevated platform, then returns to face forward.
- 名称：small_light_one_hand_put_down_right_side_high_R；时长 4.37s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_one_hand_put_down_right_side_high_R_001__A517.csv`

### big_light_two_hands_put_down_right_side_high_R_001__A520
- 说明：A person holding an object places it to their right and stands idle.
- 名称：big_light_two_hands_put_down_right_side_high_R；时长 7.56s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_two_hands_put_down_right_side_high_R_001__A520.csv`

### medium_big_light_two_hands_put_down_front_high_R_001__A529
- 说明：A standing person puts a medium, light object high up in front of them using both hands, then returns their arms to their sides.
- 名称：medium_big_light_two_hands_put_down_front_high_R；时长 6.38s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231121/medium_big_light_two_hands_put_down_front_high_R_001__A529.csv`

### big_light_one_hand_put_down_behind_high_R_001__A523
- 说明：A person puts down a light object with their right hand to the high-up behind.
- 名称：big_light_one_hand_put_down_behind_high_R；时长 5.73s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_one_hand_put_down_behind_high_R_001__A523.csv`

### crutches_put_away_R_fast_002__A519
- 说明：A person bends down slowly in the forward direction to put away their crutches, then gets up and stands still.
- 名称：crutches_put_away_R_fast；时长 3.37s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/crutches_put_away_R_fast_002__A519.csv`

### big_light_two_hands_put_down_front_high_R_002__A522
- 说明：A person is lifting up an object with both hands and placing it high up towards the front.
- 名称：big_light_two_hands_put_down_front_high_R；时长 4.09s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_two_hands_put_down_front_high_R_002__A522.csv`

### medium_big_light_one_hand_put_down_front_medium_R_001__A510
- 说明：A person lifts a large, light object placed in front at head level and then moves it to place it down at a medium height in front of them.
- 名称：medium_big_light_one_hand_put_down_front_medium_R；时长 3.20s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_one_hand_put_down_front_medium_R_001__A510.csv`

### medium_light_two_hands_put_down_behind_high_R_001__A527
- 说明：A person puts down a medium-light object with their two hands from high up behind and then stands upright.
- 名称：medium_light_two_hands_put_down_behind_high_R；时长 8.61s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_light_two_hands_put_down_behind_high_R_001__A527.csv`

### medium_big_light_two_hands_put_down_front_medium_R_001__A511
- 说明：A person puts down a light, medium-sized object in front with two hands and then stands in an upright position.
- 名称：medium_big_light_two_hands_put_down_front_medium_R；时长 5.53s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_put_down_front_medium_R_001__A511.csv`

### small_light_two_hands_put_down_front_high_R_001__A516
- 说明：A person holding a small object with both hands puts it down forward at head level.
- 名称：small_light_two_hands_put_down_front_high_R；时长 1.96s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_two_hands_put_down_front_high_R_001__A516.csv`

### big_light_two_hands_put_down_front_medium_R_001__A508
- 说明：A person holding a big object with hands raised forward at torso height places it in front of them and lowers their hands.
- 名称：big_light_two_hands_put_down_front_medium_R；时长 4.20s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_put_down_front_medium_R_001__A508.csv`

### big_light_one_hand_put_down_right_side_high_R_002__A521
- 说明：A person is holding an object with the right hand, placing it upward to the right, and then lowering the hand.
- 名称：big_light_one_hand_put_down_right_side_high_R；时长 5.48s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_one_hand_put_down_right_side_high_R_002__A521.csv`

### medium_light_two_hands_put_down_behind_medium_R_001__A510
- 说明：A person turns behind to place an object at a medium height behind them and then again turns forward.
- 名称：medium_light_two_hands_put_down_behind_medium_R；时长 6.77s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/medium_light_two_hands_put_down_behind_medium_R_001__A510.csv`

### medium_big_light_two_hands_put_down_right_side_low_R_002__A508
- 说明：A person holding a light, medium-sized object with two hands puts it down to their right before getting up and facing forward in an upright position.
- 名称：medium_big_light_two_hands_put_down_right_side_low_R；时长 6.83s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_put_down_right_side_low_R_002__A508.csv`

### small_light_two_hands_put_down_right_side_high_R_001__A516
- 说明：A person turns right while lifting their arms to place a small, light object with both hands at the upper right side before standing upright and facing forward.
- 名称：small_light_two_hands_put_down_right_side_high_R；时长 3.12s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_two_hands_put_down_right_side_high_R_001__A516.csv`

### medium_light_two_hands_put_down_right_side_high_R_001__A527
- 说明：A person standing upright, holding a medium-light object with both hands, quickly places it at a higher level to their right.
- 名称：medium_light_two_hands_put_down_right_side_high_R；时长 5.04s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_light_two_hands_put_down_right_side_high_R_001__A527.csv`

### medium_light_two_hands_put_down_front_medium_R_002__A511
- 说明：A person puts down an object held in their hands to their right side at medium height and stands upright.
- 名称：medium_light_two_hands_put_down_front_medium_R；时长 4.03s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_light_two_hands_put_down_front_medium_R_002__A511.csv`

### big_light_one_hand_put_down_behind_medium_R_003__A508
- 说明：A person lifting an object at a medium level turns around from the right, puts it down at the same level with one hand, and then turns forward.
- 名称：big_light_one_hand_put_down_behind_medium_R；时长 5.82s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_put_down_behind_medium_R_003__A508.csv`

### medium_big_light_one_hand_put_down_behind_medium_R_001__A508
- 说明：A person standing upright turns to their right, places the large object behind them, and then turns back to face forward.
- 名称：medium_big_light_one_hand_put_down_behind_medium_R；时长 7.33s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_one_hand_put_down_behind_medium_R_001__A508.csv`

### medium_light_two_hands_put_down_front_high_R_001__A524
- 说明：A person places a medium, light object on a high platform in the front with their hands and stands in an idle posture after relaxing the arms.
- 名称：medium_light_two_hands_put_down_front_high_R；时长 4.53s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_light_two_hands_put_down_front_high_R_001__A524.csv`

### big_light_one_hand_put_down_right_side_low_R_003__A511
- 说明：A person slowly puts down an object with their hand on their right side at their waist level.
- 名称：big_light_one_hand_put_down_right_side_low_R；时长 4.45s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_put_down_right_side_low_R_003__A511.csv`

### small_light_two_hands_put_down_behind_low_R_001__A506
- 说明：A person turns over their right shoulder, places a small, light object with both hands at a low height behind them, then turns around and stands in a place.
- 名称：small_light_two_hands_put_down_behind_low_R；时长 4.13s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231113/small_light_two_hands_put_down_behind_low_R_001__A506.csv`

### big_light_two_hands_put_down_behind_medium_R_001__A509
- 说明：A person rotates 180 degrees in clockwise direction, puts down an object and then rotates in an anti-clockwise direction.
- 名称：big_light_two_hands_put_down_behind_medium_R；时长 7.20s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_put_down_behind_medium_R_001__A509.csv`

### small_light_one_hand_put_down_front_high_R_001__A519
- 说明：A person puts a small object in their right hand in front at the head level before standing still.
- 名称：small_light_one_hand_put_down_front_high_R；时长 4.83s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_one_hand_put_down_front_high_R_001__A519.csv`

### small_light_two_hands_put_down_right_side_low_R_001__A507
- 说明：A person puts down a small, light object held in front of them with both hands to the floor on the right side, then quickly straightens and stands upright.
- 名称：small_light_two_hands_put_down_right_side_low_R；时长 7.20s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231113/small_light_two_hands_put_down_right_side_low_R_001__A507.csv`

### medium_big_light_two_hands_put_down_behind_low_R_001__A509
- 说明：The person partially kneels down while turning around, places a light object behind them, then turns back and stands up.
- 名称：medium_big_light_two_hands_put_down_behind_low_R；时长 6.95s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_put_down_behind_low_R_001__A509.csv`

### small_light_two_hands_put_down_front_low_R_001__A507
- 说明：A person standing upright, holding a small light object with both hands, bends down, places it down and then stands still.
- 名称：small_light_two_hands_put_down_front_low_R；时长 5.99s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231113/small_light_two_hands_put_down_front_low_R_001__A507.csv`

### medium_light_two_hands_put_down_behind_low_R_001__A506
- 说明：A person is quickly turning to their behind, placing an object at a low height before returning to a balanced stance.
- 名称：medium_light_two_hands_put_down_behind_low_R；时长 4.54s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231113/medium_light_two_hands_put_down_behind_low_R_001__A506.csv`

### big_light_two_hands_put_down_front_low_R_001__A511
- 说明：A person is bending and placing down an object with both hands from a low height in front of them and straightening their back.
- 名称：big_light_two_hands_put_down_front_low_R；时长 4.53s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_put_down_front_low_R_001__A511.csv`

### small_light_one_hand_put_down_right_side_medium_R_002__A510
- 说明：A person places a small object down to their right at medium height and then returns to a neutral standing position.
- 名称：small_light_one_hand_put_down_right_side_medium_R；时长 4.49s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/small_light_one_hand_put_down_right_side_medium_R_002__A510.csv`

### medium_big_light_two_hands_put_down_right_side_high_R_001__A529
- 说明：A standing person turns to their right, places an object on an elevated surface, and then lowers their arms and stands upright.
- 名称：medium_big_light_two_hands_put_down_right_side_high_R；时长 5.12s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231121/medium_big_light_two_hands_put_down_right_side_high_R_001__A529.csv`

### medium_big_light_two_hands_put_down_right_side_medium_R_002__A509
- 说明：A person holding a big and light object in their hands gently places it on a medium high platform behind them.
- 名称：medium_big_light_two_hands_put_down_behind_medium_R；时长 5.42s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_put_down_right_side_medium_R_002__A509.csv`

### crutch_put_away_R_slow_002__A519
- 说明：A person slowly moves a single crutch and then places it down on the floor before straightening up slightly, remaining tilted to the left side.
- 名称：crutch_put_away_R_slow；时长 7.57s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸
- CSV：`curated_600/motions/g1/csv/231116/crutch_put_away_R_slow_002__A519.csv`

### neutral_item_put_away_R_001__A544
- 说明：A person puts an item away behind the torso with their right hand.
- 名称：neutral_item_put_away_R；时长 5.99s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/240529/neutral_item_put_away_R_001__A544.csv`

### big_light_one_hand_put_down_front_high_R_001__A522
- 说明：A person puts down a big object with one hand from high upfront.
- 名称：big_light_one_hand_put_down_front_high_R；时长 6.03s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_one_hand_put_down_front_high_R_001__A522.csv`

### medium_big_light_one_hand_put_down_right_side_low_R_001__A504
- 说明：A person standing upright while holding a medium-sized light object with their right hand gently puts it down to their right.
- 名称：medium_big_light_one_hand_put_down_right_side_low_R；时长 3.08s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231113/medium_big_light_one_hand_put_down_right_side_low_R_001__A504.csv`

### small_light_two_hands_put_down_behind_high_R_001__A518
- 说明：A person turns back over their right shoulder, holding a small, light object in their hands and puts it on the shelf high in the back.
- 名称：small_light_two_hands_put_down_behind_high_R；时长 3.38s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_two_hands_put_down_behind_high_R_001__A518.csv`

### medium_big_light_two_hands_put_down_right_side_medium_R_001__A508
- 说明：The person turns to the right and puts the medium, light object at their right with two hands from medium height and turns back to normal stance.
- 名称：medium_big_light_two_hands_put_down_right_side_medium_R；时长 4.27s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_put_down_right_side_medium_R_001__A508.csv`

### medium_big_light_two_hands_put_down_front_high_R_001__A528
- 说明：A standing person puts a medium, light object high up in front of them using both hands, then returns their arms to their sides.
- 名称：medium_big_light_two_hands_put_down_front_high_R；时长 4.55s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231121/medium_big_light_two_hands_put_down_front_high_R_001__A528.csv`

### small_light_one_hand_put_down_behind_high_R_002__A517
- 说明：A person turns around, raises and extends their right arm to place a light object at a high level.
- 名称：small_light_one_hand_put_down_behind_high_R；时长 2.78s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_one_hand_put_down_behind_high_R_002__A517.csv`

### medium_big_light_two_hands_put_down_behind_high_R_001__A529
- 说明：A person holding an object with both hands turns around over their right shoulder, places it on the top shelf, and then stands upright.
- 名称：medium_big_light_two_hands_put_down_behind_high_R；时长 5.67s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231121/medium_big_light_two_hands_put_down_behind_high_R_001__A529.csv`

### big_light_one_hand_put_down_behind_high_R_001__A520
- 说明：A person puts down a light object with their right hand to the high-up behind.
- 名称：big_light_one_hand_put_down_behind_high_R；时长 6.14s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_one_hand_put_down_behind_high_R_001__A520.csv`

### medium_big_light_one_hand_put_down_behind_high_R_001__A526
- 说明：A person holding an object in their right hand turns right and places it on a higher shelf behind them, then lowers the hand and faces forward.
- 名称：medium_big_light_one_hand_put_down_behind_high_R；时长 4.15s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_big_light_one_hand_put_down_behind_high_R_001__A526.csv`

### big_light_one_hand_put_down_right_side_medium_R_001__A511
- 说明：A person uses their right hand to place an object at medium height on their right side.
- 名称：big_light_one_hand_put_down_right_side_medium_R；时长 3.37s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_put_down_right_side_medium_R_001__A511.csv`

### big_light_two_hands_put_down_behind_high_R_001__A523
- 说明：A person holding a big object turns around and puts it high up behind them before turning back to face forward.
- 名称：big_light_two_hands_put_down_behind_high_R；时长 5.32s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_two_hands_put_down_behind_high_R_001__A523.csv`

### medium_light_two_hands_put_down_behind_high_R_001__A526
- 说明：A person holding a light object at chest level quickly turns backward and places it on a high platform behind them then turns forward to stand upright.
- 名称：medium_light_two_hands_put_down_behind_high_R；时长 5.62s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_light_two_hands_put_down_behind_high_R_001__A526.csv`

### medium_big_light_one_hand_put_down_right_side_high_R_001__A526
- 说明：A person holding an object in their right hand places it high to the right, then lowers the hand and stands still.
- 名称：medium_big_light_one_hand_put_down_right_side_high_R；时长 4.12s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_big_light_one_hand_put_down_right_side_high_R_001__A526.csv`

### small_light_two_hands_put_down_right_side_high_R_001__A517
- 说明：A person turns right while lifting their arms to place a small, light object with both hands at the upper right side before standing upright and facing forward.
- 名称：small_light_two_hands_put_down_right_side_high_R；时长 2.42s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/small_light_two_hands_put_down_right_side_high_R_001__A517.csv`

### crutches_put_away_R_fast_002__A517
- 说明：A person quickly removes the crutches from their hands and puts them down on the ground.
- 名称：crutches_put_away_R_fast；时长 5.04s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231116/crutches_put_away_R_fast_002__A517.csv`

### big_light_one_hand_put_down_behind_low_R_002__A510
- 说明：A person holding an object turns to their right, drops the object, and then turns left to face forward before standing still.
- 名称：big_light_one_hand_put_down_behind_low_R；时长 7.85s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_put_down_behind_low_R_002__A510.csv`

### medium_big_light_one_hand_put_down_behind_medium_R_001__A510
- 说明：A person turns back to put a big, light object in the right hand behind at a medium height, then lowers their hand and stands upright.
- 名称：medium_big_light_one_hand_put_down_behind_medium_R；时长 5.02s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_one_hand_put_down_behind_medium_R_001__A510.csv`

### medium_big_light_one_hand_put_down_front_high_R_002__A526
- 说明：A person holding an object in their right hand in front of their chest raises their right arm and places the object on an overhead shelf in front.
- 名称：medium_big_light_one_hand_put_down_front_high_R；时长 4.75s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_big_light_one_hand_put_down_front_high_R_002__A526.csv`

### medium_big_light_one_hand_put_down_front_medium_R_001__A509
- 说明：A person holding an object places it in front of them at a high level with their right hand.
- 名称：medium_big_light_one_hand_put_down_front_medium_R；时长 2.91s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_one_hand_put_down_front_medium_R_001__A509.csv`

### big_light_two_hands_put_down_behind_low_R_001__A508
- 说明：A person turns to their right and places the big, lightweight object while holding it with both hands at a low height behind them.
- 名称：big_light_two_hands_put_down_behind_low_R；时长 7.88s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_put_down_behind_low_R_001__A508.csv`

### medium_big_light_two_hands_put_down_front_medium_R_001__A510
- 说明：The person holding an object places it down in front and then stands in an upright position.
- 名称：medium_big_light_two_hands_put_down_front_medium_R；时长 7.79s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_put_down_front_medium_R_001__A510.csv`

### big_light_two_hands_put_down_right_side_low_R_001__A508
- 说明：A person is placing an object down at a low height to their right with their both hands.
- 名称：big_light_two_hands_put_down_right_side_low_R；时长 9.28s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_put_down_right_side_low_R_001__A508.csv`

### big_light_one_hand_put_down_right_side_low_R_003__A509
- 说明：A person lowers an object from a medium height in front to a lower height on their right side and then stands idle.
- 名称：big_light_one_hand_put_down_right_side_low_R；时长 5.82s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_put_down_right_side_low_R_003__A509.csv`

### big_light_two_hands_put_down_right_side_high_R_001__A523
- 说明：A person keeps a big object at a height to the right and turns to stand upright, facing forward.
- 名称：big_light_two_hands_put_down_right_side_high_R；时长 7.04s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231117/big_light_two_hands_put_down_right_side_high_R_001__A523.csv`

### big_light_one_hand_put_down_front_medium_R_002__A508
- 说明：A person places an object on a moderately high platform in front.
- 名称：big_light_one_hand_put_down_front_medium_R；时长 3.15s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_put_down_front_medium_R_002__A508.csv`

### medium_light_two_hands_put_down_front_high_R_001__A525
- 说明：A person places a light object on an elevated surface, then lowers their arms, brings their hands together, and rests their forearms at the sides.
- 名称：medium_light_two_hands_put_down_front_high_R；时长 3.51s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231120/medium_light_two_hands_put_down_front_high_R_001__A525.csv`

### big_light_one_hand_put_down_behind_medium_R_003__A509
- 说明：A person holds an object, turns backward, places the object, then turns forward and stands upright.
- 名称：big_light_one_hand_put_down_behind_medium_R；时长 4.36s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_put_down_behind_medium_R_003__A509.csv`

### small_light_two_hands_put_down_behind_medium_R_001__A511
- 说明：A person holds a small object at medium height with both hands, quickly places it behind while turning over the right shoulder, and then turns back.
- 名称：small_light_two_hands_put_down_behind_medium_R；时长 4.04s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/small_light_two_hands_put_down_behind_medium_R_001__A511.csv`

### medium_big_light_one_hand_put_down_front_low_R_001__A504
- 说明：The person extends the right hand to picks the object at the front and puts it lower in front while facing forward.
- 名称：medium_big_light_one_hand_put_down_front_low_R；时长 3.38s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾
- CSV：`curated_600/motions/g1/csv/231113/medium_big_light_one_hand_put_down_front_low_R_001__A504.csv`

### big_light_two_hands_put_down_behind_medium_R_001__A511
- 说明：A person holding an object with hands raised forward at chest height turns backward to place the object down at a medium height.
- 名称：big_light_two_hands_put_down_behind_medium_R；时长 5.54s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_put_down_behind_medium_R_001__A511.csv`

### big_light_two_hands_put_down_front_medium_R_001__A511
- 说明：A person is placing an object at a medium height in the front with both hands and then lowering their arms.
- 名称：big_light_two_hands_put_down_front_medium_R；时长 3.25s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_put_down_front_medium_R_001__A511.csv`

## 持物姿态：33 条

### petting_cat_standing_R_002__A533
- 说明：A person standing upright and holding a cat in their left arm starts petting it steadily with their right arm.
- 名称：petting_cat_holding_R；时长 7.40s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/240327/petting_cat_standing_R_002__A533.csv`

### big_light_two_hands_hold_long_R_001__A511
- 说明：A person stands and holds a big, light object with two hands for a long period with both arms.
- 名称：big_light_two_hands_hold_long_R；时长 33.19s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_hold_long_R_001__A511.csv`

### passenger_hold_high_bus_R_001__A456
- 说明：A person grips a high rail while standing on the bus and then gradually brings their hand down.
- 名称：passenger_hold_high_bus_R；时长 12.31s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231004/passenger_hold_high_bus_R_001__A456.csv`

### medium_light_two_hands_hold_long_R_001__A505
- 说明：A person holding an object in their hands sways to the sides.
- 名称：medium_light_two_hands_hold_long_R；时长 26.36s；保留该命名动作家族的典型版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/231113/medium_light_two_hands_hold_long_R_001__A505.csv`

### big_light_two_hands_hold_R_001__A510
- 说明：A person standing still moves slightly while holding a big object in their hands.
- 名称：big_light_two_hands_hold_R；时长 11.19s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_hold_R_001__A510.csv`

### medium_big_light_two_hands_hold_R_001__A508
- 说明：A person stands still while holding a medium-sized object with both hands under it, raised in front of their torso.
- 名称：medium_big_light_two_hands_hold_R；时长 8.63s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_hold_R_001__A508.csv`

### small_light_one_hand_hold_long_001__A506
- 说明：A person is holding an object with their right hand.
- 名称：small_light_one_hand_hold_long_R；时长 21.22s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231113/small_light_one_hand_hold_long_001__A506.csv`

### medium_light_two_hands_hold_R_001__A504
- 说明：A person is standing upright and holding an object with both hands at the medium level in front of them.
- 名称：medium_light_two_hands_hold_R；时长 11.41s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231113/medium_light_two_hands_hold_R_001__A504.csv`

### medium_big_light_two_hands_hold_long_R_001__A509
- 说明：A person holding a big object with both hands at torso level leans to the left and right before regaining their stance.
- 名称：medium_big_light_two_hands_hold_long_R；时长 33.26s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_hold_long_R_001__A509.csv`

### passenger_hold_high_bus_R_001__A459
- 说明：An upright person raises their right arm, holds the handrail in the bus, stands for a while, and then lowers their hand.
- 名称：passenger_hold_high_bus_R；时长 12.45s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231004/passenger_hold_high_bus_R_001__A459.csv`

### small_light_one_hand_hold_001__A505
- 说明：The person stands still, holding a small light object in their right hand while facing forward.
- 名称：small_light_one_hand_hold_R；时长 13.82s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231113/small_light_one_hand_hold_001__A505.csv`

### big_light_one_hand_hold_R_001__A511
- 说明：A person holding an object sways slightly.
- 名称：big_light_one_hand_hold_R；时长 15.28s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_hold_R_001__A511.csv`

### small_light_two_hands_hold_long_R_002__A507
- 说明：A person steadily leans to the right and then to the left while holding an object in both hands for a long period.
- 名称：small_light_two_hands_hold_long_R；时长 24.18s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231113/small_light_two_hands_hold_long_R_002__A507.csv`

### medium_big_light_one_hand_hold_R_001__A505
- 说明：The person firmly holds a medium-sized object with one hand.
- 名称：medium_big_light_one_hand_hold_R；时长 12.03s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231113/medium_big_light_one_hand_hold_R_001__A505.csv`

### big_light_one_hand_hold_long_R_001__A511
- 说明：A person holds a big object for a long period of time with the right hand.
- 名称：big_light_one_hand_hold_long_R；时长 29.76s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_hold_long_R_001__A511.csv`

### medium_light_two_hands_hold_long_R_001__A507
- 说明：A person is holding a medium-light object with both hands for an extended period. The person moves their body while maintaining the hold.
- 名称：medium_light_two_hands_hold_long_R；时长 32.31s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231113/medium_light_two_hands_hold_long_R_001__A507.csv`

### big_light_two_hands_hold_long_R_001__A508
- 说明：A person holding a big object with both hands raised forward stumbles and moves unenergetically.
- 名称：big_light_two_hands_hold_long_R；时长 34.25s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_hold_long_R_001__A508.csv`

### medium_light_two_hands_hold_R_001__A505
- 说明：A person is standing upright and holding an object with both hands at the medium level in front of them.
- 名称：medium_light_two_hands_hold_R；时长 11.41s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/231113/medium_light_two_hands_hold_R_001__A505.csv`

### medium_big_light_one_hand_hold_long_R_002__A507
- 说明：A person holds an object with their one hand for a long period of time and tilts their hips from side to side, then stands straight.
- 名称：medium_big_light_one_hand_hold_long_R；时长 30.41s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231113/medium_big_light_one_hand_hold_long_R_002__A507.csv`

### passenger_hold_high_bus_R_001__A458
- 说明：A person grips a high rail while standing on the bus and then gradually brings their hand down.
- 名称：passenger_hold_high_bus_R；时长 14.82s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231004/passenger_hold_high_bus_R_001__A458.csv`

### big_light_two_hands_hold_R_001__A509
- 说明：The person stands still with their arms extended outward while holding an object.
- 名称：big_light_two_hands_hold_R；时长 13.03s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_hold_R_001__A509.csv`

### small_light_two_hands_hold_R_001__A504
- 说明：The person is standing idle while holding a small, light object with two hands.
- 名称：small_light_two_hands_hold_R；时长 7.74s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/231113/small_light_two_hands_hold_R_001__A504.csv`

### medium_big_light_two_hands_hold_long_R_001__A511
- 说明：A person holding an object in front of their torso with both their hands is swaying from side to side.
- 名称：medium_big_light_two_hands_hold_long_R；时长 29.00s；保留该命名动作家族的典型版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_hold_long_R_001__A511.csv`

### big_light_one_hand_hold_long_R_001__A508
- 说明：The person shifts, bends, and straightens the torso several times, bends over once, and stands still, all while holding an object with their right hand.
- 名称：big_light_one_hand_hold_long_R；时长 31.14s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_hold_long_R_001__A508.csv`

### small_light_two_hands_hold_long_R_002__A504
- 说明：A person is standing and shifting weight while holding a small, light object with both hands.
- 名称：small_light_two_hands_hold_long_R；时长 29.94s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/231113/small_light_two_hands_hold_long_R_002__A504.csv`

### small_light_two_hands_hold_R_001__A506
- 说明：A person standing with a small, light object in front of their chest with both hands sways slightly.
- 名称：small_light_two_hands_hold_R；时长 6.51s；保留该命名动作家族的典型版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/231113/small_light_two_hands_hold_R_001__A506.csv`

### big_light_two_hands_hold_long_R_001__A509
- 说明：A person holds a light object with both hands for a long period, moving it up and down repeatedly.
- 名称：big_light_two_hands_hold_long_R；时长 41.74s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_two_hands_hold_long_R_001__A509.csv`

### medium_big_light_two_hands_hold_long_R_001__A510
- 说明：A person steadily leans to the right and then to the left while holding an object in both hands for a long period.
- 名称：medium_big_light_two_hands_hold_long_R；时长 36.40s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/medium_big_light_two_hands_hold_long_R_001__A510.csv`

### small_light_one_hand_hold_long_001__A505
- 说明：The person stands holding a small, light object in the right hand, moving with low energy as they lazily sway left, right, forward, and backward with small bounces.
- 名称：small_light_one_hand_hold_long_R；时长 24.22s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231113/small_light_one_hand_hold_long_001__A505.csv`

### medium_big_light_one_hand_hold_long_R_002__A505
- 说明：A person is holding a medium-sized, lightweight object with their right hand in front at chest level, gently swaying their body left and right.
- 名称：medium_big_light_one_hand_hold_long_R；时长 32.37s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231113/medium_big_light_one_hand_hold_long_R_002__A505.csv`

### small_light_two_hands_hold_long_R_002__A506
- 说明：A person is standing and shifting weight while holding a small, light object with both hands.
- 名称：small_light_two_hands_hold_long_R；时长 25.51s；保留该命名动作家族的典型版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/231113/small_light_two_hands_hold_long_R_002__A506.csv`

### medium_light_two_hands_hold_long_R_001__A504
- 说明：A person stands while holding an object in their hands for a long period of time.
- 名称：medium_light_two_hands_hold_long_R；时长 34.25s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231113/medium_light_two_hands_hold_long_R_001__A504.csv`

### big_light_one_hand_hold_long_R_001__A510
- 说明：The person shifts, bends, and straightens the torso several times, bends over once, and stands still, all while holding an object with their right hand.
- 名称：big_light_one_hand_hold_long_R；时长 34.34s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231114/big_light_one_hand_hold_long_R_001__A510.csv`

## 伸手够取：25 条

### reaching_down_R_002__A056
- 说明：A person reaches down while extending their right arm downward and then rises to an upright position.
- 名称：reaching_down_R；时长 6.75s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/221012/reaching_down_R_002__A056.csv`

### reaching_up_R_003__A269
- 说明：A person raises their right arm to reach up and carefully search for something.
- 名称：reaching_up_R；时长 11.88s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230314/reaching_up_R_003__A269.csv`

### reaching_up_R_004__A099
- 说明：A person raises their right arm to reach up and carefully search for something.
- 名称：reaching_up_R；时长 5.47s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230103/reaching_up_R_004__A099.csv`

### reaching_far_R_002__A409
- 说明：An upright person bends forward and stretches their right hand to reach far at torso level, then lowers it down and stands upright.
- 名称：reaching_far_R；时长 13.54s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230529/reaching_far_R_002__A409.csv`

### reaching_down_R_002__A071
- 说明：A person gradually bends forward, reaching their right hand to the ground.
- 名称：reaching_down_R；时长 8.54s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/221118/reaching_down_R_002__A071.csv`

### reaching_far_R_001__A271
- 说明：A person is standing and reaching far while moving their right hand forward.
- 名称：reaching_far_R；时长 12.15s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230314/reaching_far_R_001__A271.csv`

### reaching_up_R_003__A098
- 说明：A person raises their right arm to reach up and carefully search for something.
- 名称：reaching_up_R；时长 10.24s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230103/reaching_up_R_003__A098.csv`

### reaching_down_R_001__A272
- 说明：A person reaches down while extending their right arm downward and then rises to an upright position.
- 名称：reaching_down_R；时长 10.24s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230314/reaching_down_R_001__A272.csv`

### reaching_far_R_002__A048
- 说明：An upright person bends forward and stretches their right hand to reach far at torso level, then lowers it down and stands upright.
- 名称：reaching_far_R；时长 4.29s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/221010/reaching_far_R_002__A048.csv`

### reaching_far_R_001__A235
- 说明：An upright person bends forward and stretches their right hand to reach far at torso level, then lowers it down and stands upright.
- 名称：reaching_far_R；时长 6.24s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230302/reaching_far_R_001__A235.csv`

### reaching_down_R_002__A140
- 说明：A person reaches down while extending their right arm downward and then rises to an upright position.
- 名称：reaching_down_R；时长 8.18s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230124/reaching_down_R_002__A140.csv`

### reaching_up_R_004__A059
- 说明：A person raises their right arm to reach up and carefully search for something.
- 名称：reaching_up_R；时长 8.12s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/221115/reaching_up_R_004__A059.csv`

### reaching_down_R_001__A058
- 说明：A person reaches down while extending their right arm downward and then rises to an upright position.
- 名称：reaching_down_R；时长 7.00s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/221115/reaching_down_R_001__A058.csv`

### reaching_far_R_003__A237
- 说明：An upright person bends forward and stretches their right hand to reach far at torso level, then lowers it down and stands upright.
- 名称：reaching_far_R；时长 6.36s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230302/reaching_far_R_003__A237.csv`

### reaching_far_R_001__A236
- 说明：An upright person bends forward and stretches their right hand to reach far at torso level, then lowers it down and stands upright.
- 名称：reaching_far_R；时长 7.28s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230302/reaching_far_R_001__A236.csv`

### reaching_far_R_003__A064
- 说明：An upright person bends forward and stretches their right hand to reach far at torso level, then lowers it down and stands upright.
- 名称：reaching_far_R；时长 7.78s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/221116/reaching_far_R_003__A064.csv`

### reaching_far_R_001__A141
- 说明：An upright person bends forward and stretches their right hand to reach far at torso level, then lowers it down and stands upright.
- 名称：reaching_far_R；时长 6.13s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230124/reaching_far_R_001__A141.csv`

### reaching_far_R_003__A099
- 说明：An upright person bends forward and stretches their right hand to reach far at torso level, then lowers it down and stands upright.
- 名称：reaching_far_R；时长 5.72s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230103/reaching_far_R_003__A099.csv`

### reaching_down_R_003__A140
- 说明：A person reaches down while extending their right arm downward and then rises to an upright position.
- 名称：reaching_down_R；时长 6.67s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230124/reaching_down_R_003__A140.csv`

### reaching_far_R_003__A049
- 说明：An upright person bends forward and stretches their right hand to reach far at torso level, then lowers it down and stands upright.
- 名称：reaching_far_R；时长 2.59s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/221011/reaching_far_R_003__A049.csv`

### reaching_far_R_003__A116
- 说明：An upright person bends forward and stretches their right hand to reach far at torso level, then lowers it down and stands upright.
- 名称：reaching_far_R；时长 6.88s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230112/reaching_far_R_003__A116.csv`

### reaching_up_R_003__A140
- 说明：A person raises their right arm to reach up and carefully search for something.
- 名称：reaching_up_R；时长 6.22s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230124/reaching_up_R_003__A140.csv`

### reaching_far_R_003__A270
- 说明：A person is standing and reaching far while moving their right hand forward.
- 名称：reaching_far_R；时长 9.05s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230314/reaching_far_R_003__A270.csv`

### reaching_far_R_003__A261
- 说明：An upright person bends forward and stretches their right hand to reach far at torso level, then lowers it down and stands upright.
- 名称：reaching_far_R；时长 11.49s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：躯干前倾、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230309/reaching_far_R_003__A261.csv`

### reaching_up_R_003__A101
- 说明：A person raises their right arm to reach up and carefully search for something.
- 名称：reaching_up_R；时长 6.42s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230103/reaching_up_R_003__A101.csv`

## 日常操作：43 条

### lift_crate_loop_001__A140
- 说明：The person stands holding a crate in front with both hands, leaning back slightly while facing forward.
- 名称：lift_crate_loop；时长 9.21s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/230124/lift_crate_loop_001__A140.csv`

### lift_crate_stop_002__A200
- 说明：An upright person lifting a crate with both hands at waist level bends forward, keeps it down, and straightens their stance.
- 名称：lift_crate_stop；时长 3.46s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230216/lift_crate_stop_002__A200.csv`

### side_lift_360_R_001__A343
- 说明：A shy person performs two squats while resting their hands back on a platform and then stands while swaying their arms.
- 名称：side_lift_360_R；时长 11.32s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态
- CSV：`curated_600/motions/g1/csv/230420/side_lift_360_R_001__A343.csv`

### wash_floor_R_002__A328
- 说明：A person is washing the floor by using both hands before standing in a place.
- 名称：wash_floor_R；时长 6.64s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230417/wash_floor_R_002__A328.csv`

### sweep_floor_front_walk_R_002__A299
- 说明：A person standing holding a broom walks forward at a normal pace while sweeping the floor with both hands, stops, and stands.
- 名称：sweep_floor_front_walk_R；时长 6.80s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230322/sweep_floor_front_walk_R_002__A299.csv`

### washing_dishes_R_004__A298
- 说明：A person washes the dishes and sets them aside while standing at their place.
- 名称：washing_dishes_R；时长 13.63s；保留该命名动作家族的典型版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/230322/washing_dishes_R_004__A298.csv`

### lift_crate_walk_ff_loop_270_002__A140
- 说明：A person walks slowly to the right with long strides, lifting a crate.
- 名称：lift_crate_walk_ff_loop_270_R；时长 13.39s；保留该命名动作家族的典型版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/230124/lift_crate_walk_ff_loop_270_002__A140.csv`

### lift_crate_start_002__A201
- 说明：A person bends down to pick up the crate with both hands and lifts it up to hold it steadily while slightly leaning back.
- 名称：lift_crate_start；时长 9.48s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230216/lift_crate_start_002__A201.csv`

### lift_crate_turn_270_002__A203
- 说明：A person lifting a crate with their hands turns to their right at a slow pace.
- 名称：lift_crate_turn_270；时长 2.54s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/230216/lift_crate_turn_270_002__A203.csv`

### sweep_floor_side_walk_R_004__A296
- 说明：A person slowly walks to the right while sweeping the floor with a broom.
- 名称：sweep_floor_side_walk_R；时长 5.84s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230322/sweep_floor_side_walk_R_004__A296.csv`

### sweep_floor_front_R_003__A326
- 说明：A person is sweeping the floor forward, then stands swaying while holding the mop.
- 名称：sweep_floor_front_R；时长 10.43s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230417/sweep_floor_front_R_003__A326.csv`

### turn_lift_crate_walk_360_002__A160
- 说明：A person standing and holding a crate turns back over their right shoulder and starts walking forward steadily.
- 名称：lift_crate_turn_walk_360；时长 15.05s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/230131/turn_lift_crate_walk_360_002__A160.csv`

### lift_crate_turn_360_002__A163
- 说明：A person, holding a wide crate down in front with both hands, slowly turns back over their right shoulder.
- 名称：lift_crate_turn_360；时长 4.47s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/230131/lift_crate_turn_360_002__A163.csv`

### lift_crate_walk_ff_stop_360_003__A142
- 说明：A person holding a crate walks slowly backwards and then stops after a while.
- 名称：lift_crate_walk_ff_stop_360_R；时长 12.28s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/230124/lift_crate_walk_ff_stop_360_003__A142.csv`

### wash_floor_360_R_004__A327
- 说明：A person holds a mop with both hands and walks backward while washing the floor with the mop before coming to a stop.
- 名称：wash_floor_360_R；时长 9.27s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/230417/wash_floor_360_R_004__A327.csv`

### lift_crate_walk_ff_start_315_003__A141
- 说明：A person lifting a crate walks backwards towards the right back diagonal at a slow pace.
- 名称：lift_crate_walk_ff_start_315_R；时长 9.68s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/230124/lift_crate_walk_ff_start_315_003__A141.csv`

### lift_crate_walk_ff_stop_225_001__A159
- 说明：A person stops walking at a slow pace towards the right diagonal while holding a crate.
- 名称：lift_crate_walk_ff_stop_225_R；时长 8.66s；保留该命名动作家族的典型版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/230131/lift_crate_walk_ff_stop_225_001__A159.csv`

### lift_crate_walk_ff_loop_315_003__A163
- 说明：A person is walking towards the right back diagonal at a slow pace, taking short steps while holding a crate with both hands in front.
- 名称：lift_crate_walk_ff_loop_315_R；时长 8.98s；保留该命名动作家族的典型版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/230131/lift_crate_walk_ff_loop_315_003__A163.csv`

### lift_crate_walk_ff_start_360_001__A140
- 说明：A person is walking backward steadily while lifting a crate with both hands.
- 名称：lift_crate_walk_ff_loop_360_R；时长 12.30s；保留该命名动作家族的典型版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/230124/lift_crate_walk_ff_start_360_001__A140.csv`

### lift_crate_walk_ff_loop_225_002__A140
- 说明：A person is walking towards their right diagonal at a slow pace while holding a crate.
- 名称：lift_crate_walk_ff_loop_225_R；时长 9.85s；保留该命名动作家族的典型版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/230124/lift_crate_walk_ff_loop_225_002__A140.csv`

### lift_crate_walk_ff_start_270_002__A163
- 说明：A person starts walking slowly to the right in a crossover pattern while holding a crate at waist level with both hands.
- 名称：lift_crate_walk_ff_start_270_R；时长 8.37s；保留该命名动作家族的典型版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/230131/lift_crate_walk_ff_start_270_002__A163.csv`

### lift_crate_walk_ff_stop_315_001__A159
- 说明：A person is slowly walking sideways to the right back diagonal and comes to a stop while holding a crate with both hands.
- 名称：lift_crate_walk_ff_stop_315_R；时长 9.50s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/230131/lift_crate_walk_ff_stop_315_001__A159.csv`

### lift_crate_walk_ff_stop_180_R_002__A159
- 说明：A person lifting a crate with their hands slowly walks forward.
- 名称：lift_crate_walk_ff_stop_180_R；时长 9.49s；保留该命名动作家族的典型版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/230131/lift_crate_walk_ff_stop_180_R_002__A159.csv`

### turn_lift_crate_walk_270_001__A142
- 说明：A person carefully lifting a crate with both hands turns to their right and walks forward.
- 名称：lift_crate_turn_walk_270；时长 8.10s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/230124/turn_lift_crate_walk_270_001__A142.csv`

### lift_crate_walk_ff_start_180_R_003__A159
- 说明：A person standing upright steadily walks in the forward direction while holding a crate in both hands.
- 名称：lift_crate_walk_ff_start_180_R；时长 10.71s；保留该命名动作家族的典型版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/230131/lift_crate_walk_ff_start_180_R_003__A159.csv`

### lift_crate_start_002__A202
- 说明：A person bends down to pick up the crate with both hands and lifts it up to hold it steadily while slightly leaning back.
- 名称：lift_crate_start；时长 10.77s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230216/lift_crate_start_002__A202.csv`

### lift_crate_stop_001__A144
- 说明：A person holding a crate places it down before returning to a balanced stance.
- 名称：lift_crate_stop；时长 3.78s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230124/lift_crate_stop_001__A144.csv`

### sweep_floor_side_walk_R_003__A327
- 说明：A person sweeps the floor while walking sideways to the right.
- 名称：sweep_floor_side_walk_R；时长 7.78s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230417/sweep_floor_side_walk_R_003__A327.csv`

### sweep_floor_front_R_002__A327
- 说明：A person is sweeping the floor forward.
- 名称：sweep_floor_front_R；时长 7.88s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230417/sweep_floor_front_R_002__A327.csv`

### lift_crate_turn_360_001__A141
- 说明：A person holding a crate with both hands in front of their hips turns back over their right shoulder at a steady, uniform pace.
- 名称：lift_crate_turn_360；时长 4.96s；保留该命名动作家族的典型版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/230124/lift_crate_turn_360_001__A141.csv`

### sweep_floor_front_walk_R_003__A328
- 说明：A person holding a mop sweeps the floor while walking forward.
- 名称：sweep_floor_front_walk_R；时长 10.12s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230417/sweep_floor_front_walk_R_003__A328.csv`

### wash_floor_360_R_004__A328
- 说明：A person holds a mop with both hands and walks backward while washing the floor with the mop before coming to a stop.
- 名称：wash_floor_360_R；时长 6.83s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230417/wash_floor_360_R_004__A328.csv`

### side_lift_360_R_005__A341
- 说明：A person lowers down, lifts an object behind them using both hands, sliding it upward, then lowers it back down and stands upright.
- 名称：side_lift_360_R；时长 11.18s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾
- CSV：`curated_600/motions/g1/csv/230420/side_lift_360_R_005__A341.csv`

### turn_lift_crate_walk_360_001__A159
- 说明：A person standing and holding a crate turns back over their right shoulder and starts walking forward steadily.
- 名称：lift_crate_turn_walk_360；时长 9.77s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/230131/turn_lift_crate_walk_360_001__A159.csv`

### lift_crate_walk_ff_loop_180_R_003__A159
- 说明：A person is walking forward slowly while lifting a crate in front with both their hands.
- 名称：lift_crate_walk_ff_loop_180_R；时长 8.65s；保留该命名动作家族的典型版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/230131/lift_crate_walk_ff_loop_180_R_003__A159.csv`

### wash_floor_R_003__A296
- 说明：A person is washing the floor with a floor mop.
- 名称：wash_floor_R；时长 8.24s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230322/wash_floor_R_003__A296.csv`

### lift_crate_walk_ff_start_360_002__A159
- 说明：A person holding a crate with both hands starts walking backward slowly.
- 名称：lift_crate_walk_ff_start_360_R；时长 11.00s；保留该命名动作家族的典型版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/230131/lift_crate_walk_ff_start_360_002__A159.csv`

### lift_crate_walk_ff_start_315_003__A163
- 说明：A person lifting a crate walks backwards towards the right back diagonal at a slow pace.
- 名称：lift_crate_walk_ff_start_315_R；时长 8.11s；保留该命名动作家族的典型版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/230131/lift_crate_walk_ff_start_315_003__A163.csv`

### sweep_floor_back_R_001__A330
- 说明：A person starts carefully sweeping the floor before returning to stand upright.
- 名称：sweep_floor_back_R；时长 7.55s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230417/sweep_floor_back_R_001__A330.csv`

### lift_crate_walk_ff_loop_360_R_002__A199
- 说明：A person is walking backward steadily while lifting a crate with both hands.
- 名称：lift_crate_walk_ff_loop_360_R；时长 11.99s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/230216/lift_crate_walk_ff_loop_360_R_002__A199.csv`

### lift_crate_walk_ff_start_225_003__A142
- 说明：A person starts walking slowly towards the right diagonal while holding a crate with both hands.
- 名称：lift_crate_walk_ff_start_225_R；时长 8.84s；保留该命名动作家族的典型版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/230124/lift_crate_walk_ff_start_225_003__A142.csv`

### turn_lift_crate_walk_270_003__A162
- 说明：A person holding a crate with both hands swiftly turns to their right and walks ahead slowly with the crate.
- 名称：lift_crate_turn_walk_270；时长 9.70s；在家族配额内保留与已选轨迹差异较大的版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/230131/turn_lift_crate_walk_270_003__A162.csv`

### lift_crate_walk_ff_stop_270_001__A159
- 说明：A person is slowly walking sideways to the right while holding a crate in their hands.
- 名称：lift_crate_walk_ff_stop_270_R；时长 10.74s；保留该命名动作家族的典型版本
- FK姿态：双手前伸
- CSV：`curated_600/motions/g1/csv/230131/lift_crate_walk_ff_stop_270_001__A159.csv`

## 推拉与按压姿态：17 条

### mid_button_push_002__A485
- 说明：A person extends their right arm forward and pushes a button in front of their torso at a steady pace.
- 名称：mid_button_push；时长 5.90s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231019/mid_button_push_002__A485.csv`

### pull_shoudler_270_standing_R_002__A432
- 说明：A person starts walking and then pulls someone's shoulder a little before returning to stand upright facing forward.
- 名称：pull_shoulder_180_walk_R；时长 24.87s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/230713/pull_shoudler_270_standing_R_002__A432.csv`

### low_button_over_push_001__A486
- 说明：A person steadily bends forward, pushes a button using the right hand, and straightens back up while standing on the ground.
- 名称：low_button_over_push；时长 7.16s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：躯干前倾
- CSV：`curated_600/motions/g1/csv/231019/low_button_over_push_001__A486.csv`

### push_obstacle_180_002__A344
- 说明：A person slowly walks forward while pushing an obstacle with both hands.
- 名称：push_obstacle_180；时长 14.89s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230420/push_obstacle_180_002__A344.csv`

### push_obstacle_360_003__A344
- 说明：A person turns around to slowly push an obstacle using their back.
- 名称：push_obstacle_360；时长 28.03s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态
- CSV：`curated_600/motions/g1/csv/230420/push_obstacle_360_003__A344.csv`

### inside_door_knob_right_side_pull_aggresively_R_001__A515
- 说明：A person raises their right hand to hold a doorknob on the left side, forcefully pulls the knob with both hands, and then lowers the hand to the side.
- 名称：inside_door_knob_right_side_pull_aggresively_R；时长 5.21s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231115/inside_door_knob_right_side_pull_aggresively_R_001__A515.csv`

### high_button_over_push_001__A482
- 说明：A person raises their right hand at the high front and presses the button before lowering their arm and standing up straight.
- 名称：high_button_over_push；时长 3.11s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231018/high_button_over_push_001__A482.csv`

### avoid_bump_push_R_003__A462
- 说明：A person walking forward tries to avoid bumping into someone and then pushes the person.
- 名称：avoid_bump_push_R；时长 9.63s；保留该命名动作家族的典型版本
- FK姿态：屈膝低姿态、双手前伸
- CSV：`curated_600/motions/g1/csv/231005/avoid_bump_push_R_003__A462.csv`

### lasso_catch_pulling_R_006__A098
- 说明：A person raises their right arm, swings a lasso overhead in a circular motion, pulls it with both hands in a catching gesture, and then stands straight.
- 名称：lasso_catch_pulling_R；时长 8.87s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/230103/lasso_catch_pulling_R_006__A098.csv`

### get_pulled_shoudler_180_standing_R_003__A430
- 说明：A person walking forward gets pulled at the shoulder and walks further firmly and then stands still.
- 名称：get_pulled_shoulder_180_walk_R；时长 16.38s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/230713/get_pulled_shoudler_180_standing_R_003__A430.csv`

### outside_door_handle_left_side_pull_R_001__A514
- 说明：A person tries to open a door with its hands. The person pulls the handle with its right hand but fails to open the door.
- 名称：outside_door_handle_left_side_pull_R；时长 4.20s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231115/outside_door_handle_left_side_pull_R_001__A514.csv`

### walk_the_dog_ff_180_pull_back_leash_R_001__A492
- 说明：A person is getting pulled forward by a dog on a leash.
- 名称：walk_the_dog_ff_180_pull_back_leash_R；时长 5.83s；保留该命名动作家族的典型版本
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231024/walk_the_dog_ff_180_pull_back_leash_R_001__A492.csv`

### high_button_under_push_001__A487
- 说明：A person presses a button placed at a high level in the front from underneath with the right hand. They then lower the arm to the side.
- 名称：high_button_under_push；时长 2.12s；pilot 50保留项；保留已人工查看的50条 pilot；不按官方 actor 通过率删数据
- FK姿态：抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231019/high_button_under_push_001__A487.csv`

### pull_shoudler_270_standing_R_001__A428
- 说明：A person stands idle, then quickly uses their right hand to pull the arm of someone standing to their right before returning to idle stance.
- 名称：pull_shoulder_270_standing_R；时长 18.87s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/230713/pull_shoudler_270_standing_R_001__A428.csv`

### walk_the_dog_ff_270_loop_R_001__A478
- 说明：A person is walking sideways to their right while holding a leash in their right hand.
- 名称：walk_the_dog_ff_270_pull_leash_R；时长 3.31s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/231011/walk_the_dog_ff_270_loop_R_001__A478.csv`

### get_pulled_shoudler_180_standing_R_002__A431
- 说明：A person standing upright, facing forward, is pulled at the left shoulder.
- 名称：get_pulled_shoulder_180_standing_R；时长 10.91s；保留该命名动作家族的典型版本
- FK姿态：未超标签阈值
- CSV：`curated_600/motions/g1/csv/230713/get_pulled_shoudler_180_standing_R_002__A431.csv`

### outside_door_handle_left_side_pull_aggresively_R_001__A512
- 说明：A person standing upright tries to forcefully pull a handle from outside, causing the hand and body to tremble with the effort.
- 名称：outside_door_handle_left_side_pull_aggresively_R；时长 4.23s；保留该命名动作家族的典型版本
- FK姿态：躯干前倾、双手前伸、抬手/高位够取
- CSV：`curated_600/motions/g1/csv/231115/outside_door_handle_left_side_pull_aggresively_R_001__A512.csv`
