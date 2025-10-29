// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from cw1q4_interfaces:srv/QuatToEuler.idl
// generated code does not contain a copyright notice

#ifndef CW1Q4_INTERFACES__SRV__DETAIL__QUAT_TO_EULER__STRUCT_H_
#define CW1Q4_INTERFACES__SRV__DETAIL__QUAT_TO_EULER__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'q'
#include "geometry_msgs/msg/detail/quaternion__struct.h"

// Struct defined in srv/QuatToEuler in the package cw1q4_interfaces.
typedef struct cw1q4_interfaces__srv__QuatToEuler_Request
{
  geometry_msgs__msg__Quaternion q;
} cw1q4_interfaces__srv__QuatToEuler_Request;

// Struct for a sequence of cw1q4_interfaces__srv__QuatToEuler_Request.
typedef struct cw1q4_interfaces__srv__QuatToEuler_Request__Sequence
{
  cw1q4_interfaces__srv__QuatToEuler_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} cw1q4_interfaces__srv__QuatToEuler_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'z'
// Member 'y'
// Member 'x'
#include "std_msgs/msg/detail/float64__struct.h"

// Struct defined in srv/QuatToEuler in the package cw1q4_interfaces.
typedef struct cw1q4_interfaces__srv__QuatToEuler_Response
{
  std_msgs__msg__Float64 z;
  std_msgs__msg__Float64 y;
  std_msgs__msg__Float64 x;
} cw1q4_interfaces__srv__QuatToEuler_Response;

// Struct for a sequence of cw1q4_interfaces__srv__QuatToEuler_Response.
typedef struct cw1q4_interfaces__srv__QuatToEuler_Response__Sequence
{
  cw1q4_interfaces__srv__QuatToEuler_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} cw1q4_interfaces__srv__QuatToEuler_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CW1Q4_INTERFACES__SRV__DETAIL__QUAT_TO_EULER__STRUCT_H_
