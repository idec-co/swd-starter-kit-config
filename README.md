# SWD® Starter Kit / EZW-CUBE / SWD® Build KIT Configuration Files

This repo contains a set of sample configuration files for the SWD Starter Kit, EZW-CUBE, and SWD Build KIT.

### Prerequisites

- `swd-services` (**`>= 0.3.0`**)

## Commissioning

[`commissioning`](./commissioning) directory contains python scripts to commission the SWD® left and right motors. It also contains a configuration file for IDEC's SE2L LiDAR.

## File List

| File Name                                               | Detail                                                                     |
| ------------------------------------------------------- | -------------------------------------------------------------------------- |
| `commissioning/commissioning.py`                        | Configuration file to change common settings for SWD                       |
| `commissioning/swd_left_4_commissioning.py`             | Configuration file to change settings for left SWD of AMR with one LiDAR   |
| `commissioning/swd_right_5_commissioning.py`            | Configuration file to change settings for right SWD of AMR with one LiDAR  |
| `commissioning/two_lidars_swd_left_4_commissioning.py`  | Configuration file to change settings for left SWD of AMR with two LiDARs  |
| `commissioning/two_lidars_swd_right_5_commissioning.py` | Configuration file to change settings for right SWD of AMR with two LiDARs |
| `commissioning/StarterKit_IDEC.hucx`                    | Configuration file of front LiDAR for SWD Starter Kit                      |
| `commissioning/EZ09J_1_Front.hucx`                      | Configuration file of front LiDAR for EZW-CUBE                             |
| `commissioning/EZ09J_2_Rear.hucx`                       | Configuration file of rear LiDAR for EZW-CUBE                              |
| `commissioning/SWDBuildKIT_Front.hucx`                  | Configuration file of front LiDAR for SWD Build KIT                        |
| `commissioning/SWDBuildKIT_Rear.hucx`                   | Configuration file of rear LiDAR for SWD Build KIT                         |

For more information about commissioning, refer to [`docs/Commissioning.md`](docs/Commissioning.md).

---

IDEC Corporation 2025
