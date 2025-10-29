// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from cw1q4_interfaces:srv/QuatToRodrigues.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "cw1q4_interfaces/srv/detail/quat_to_rodrigues__rosidl_typesupport_introspection_c.h"
#include "cw1q4_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "cw1q4_interfaces/srv/detail/quat_to_rodrigues__functions.h"
#include "cw1q4_interfaces/srv/detail/quat_to_rodrigues__struct.h"


// Include directives for member types
// Member `q`
#include "geometry_msgs/msg/quaternion.h"
// Member `q`
#include "geometry_msgs/msg/detail/quaternion__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void QuatToRodrigues_Request__rosidl_typesupport_introspection_c__QuatToRodrigues_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  cw1q4_interfaces__srv__QuatToRodrigues_Request__init(message_memory);
}

void QuatToRodrigues_Request__rosidl_typesupport_introspection_c__QuatToRodrigues_Request_fini_function(void * message_memory)
{
  cw1q4_interfaces__srv__QuatToRodrigues_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember QuatToRodrigues_Request__rosidl_typesupport_introspection_c__QuatToRodrigues_Request_message_member_array[1] = {
  {
    "q",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(cw1q4_interfaces__srv__QuatToRodrigues_Request, q),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers QuatToRodrigues_Request__rosidl_typesupport_introspection_c__QuatToRodrigues_Request_message_members = {
  "cw1q4_interfaces__srv",  // message namespace
  "QuatToRodrigues_Request",  // message name
  1,  // number of fields
  sizeof(cw1q4_interfaces__srv__QuatToRodrigues_Request),
  QuatToRodrigues_Request__rosidl_typesupport_introspection_c__QuatToRodrigues_Request_message_member_array,  // message members
  QuatToRodrigues_Request__rosidl_typesupport_introspection_c__QuatToRodrigues_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  QuatToRodrigues_Request__rosidl_typesupport_introspection_c__QuatToRodrigues_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t QuatToRodrigues_Request__rosidl_typesupport_introspection_c__QuatToRodrigues_Request_message_type_support_handle = {
  0,
  &QuatToRodrigues_Request__rosidl_typesupport_introspection_c__QuatToRodrigues_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_cw1q4_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, cw1q4_interfaces, srv, QuatToRodrigues_Request)() {
  QuatToRodrigues_Request__rosidl_typesupport_introspection_c__QuatToRodrigues_Request_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Quaternion)();
  if (!QuatToRodrigues_Request__rosidl_typesupport_introspection_c__QuatToRodrigues_Request_message_type_support_handle.typesupport_identifier) {
    QuatToRodrigues_Request__rosidl_typesupport_introspection_c__QuatToRodrigues_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &QuatToRodrigues_Request__rosidl_typesupport_introspection_c__QuatToRodrigues_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "cw1q4_interfaces/srv/detail/quat_to_rodrigues__rosidl_typesupport_introspection_c.h"
// already included above
// #include "cw1q4_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "cw1q4_interfaces/srv/detail/quat_to_rodrigues__functions.h"
// already included above
// #include "cw1q4_interfaces/srv/detail/quat_to_rodrigues__struct.h"


// Include directives for member types
// Member `x`
// Member `y`
// Member `z`
#include "std_msgs/msg/float64.h"
// Member `x`
// Member `y`
// Member `z`
#include "std_msgs/msg/detail/float64__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void QuatToRodrigues_Response__rosidl_typesupport_introspection_c__QuatToRodrigues_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  cw1q4_interfaces__srv__QuatToRodrigues_Response__init(message_memory);
}

void QuatToRodrigues_Response__rosidl_typesupport_introspection_c__QuatToRodrigues_Response_fini_function(void * message_memory)
{
  cw1q4_interfaces__srv__QuatToRodrigues_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember QuatToRodrigues_Response__rosidl_typesupport_introspection_c__QuatToRodrigues_Response_message_member_array[3] = {
  {
    "x",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(cw1q4_interfaces__srv__QuatToRodrigues_Response, x),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "y",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(cw1q4_interfaces__srv__QuatToRodrigues_Response, y),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "z",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(cw1q4_interfaces__srv__QuatToRodrigues_Response, z),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers QuatToRodrigues_Response__rosidl_typesupport_introspection_c__QuatToRodrigues_Response_message_members = {
  "cw1q4_interfaces__srv",  // message namespace
  "QuatToRodrigues_Response",  // message name
  3,  // number of fields
  sizeof(cw1q4_interfaces__srv__QuatToRodrigues_Response),
  QuatToRodrigues_Response__rosidl_typesupport_introspection_c__QuatToRodrigues_Response_message_member_array,  // message members
  QuatToRodrigues_Response__rosidl_typesupport_introspection_c__QuatToRodrigues_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  QuatToRodrigues_Response__rosidl_typesupport_introspection_c__QuatToRodrigues_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t QuatToRodrigues_Response__rosidl_typesupport_introspection_c__QuatToRodrigues_Response_message_type_support_handle = {
  0,
  &QuatToRodrigues_Response__rosidl_typesupport_introspection_c__QuatToRodrigues_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_cw1q4_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, cw1q4_interfaces, srv, QuatToRodrigues_Response)() {
  QuatToRodrigues_Response__rosidl_typesupport_introspection_c__QuatToRodrigues_Response_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Float64)();
  QuatToRodrigues_Response__rosidl_typesupport_introspection_c__QuatToRodrigues_Response_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Float64)();
  QuatToRodrigues_Response__rosidl_typesupport_introspection_c__QuatToRodrigues_Response_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Float64)();
  if (!QuatToRodrigues_Response__rosidl_typesupport_introspection_c__QuatToRodrigues_Response_message_type_support_handle.typesupport_identifier) {
    QuatToRodrigues_Response__rosidl_typesupport_introspection_c__QuatToRodrigues_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &QuatToRodrigues_Response__rosidl_typesupport_introspection_c__QuatToRodrigues_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "cw1q4_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "cw1q4_interfaces/srv/detail/quat_to_rodrigues__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers cw1q4_interfaces__srv__detail__quat_to_rodrigues__rosidl_typesupport_introspection_c__QuatToRodrigues_service_members = {
  "cw1q4_interfaces__srv",  // service namespace
  "QuatToRodrigues",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // cw1q4_interfaces__srv__detail__quat_to_rodrigues__rosidl_typesupport_introspection_c__QuatToRodrigues_Request_message_type_support_handle,
  NULL  // response message
  // cw1q4_interfaces__srv__detail__quat_to_rodrigues__rosidl_typesupport_introspection_c__QuatToRodrigues_Response_message_type_support_handle
};

static rosidl_service_type_support_t cw1q4_interfaces__srv__detail__quat_to_rodrigues__rosidl_typesupport_introspection_c__QuatToRodrigues_service_type_support_handle = {
  0,
  &cw1q4_interfaces__srv__detail__quat_to_rodrigues__rosidl_typesupport_introspection_c__QuatToRodrigues_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, cw1q4_interfaces, srv, QuatToRodrigues_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, cw1q4_interfaces, srv, QuatToRodrigues_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_cw1q4_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, cw1q4_interfaces, srv, QuatToRodrigues)() {
  if (!cw1q4_interfaces__srv__detail__quat_to_rodrigues__rosidl_typesupport_introspection_c__QuatToRodrigues_service_type_support_handle.typesupport_identifier) {
    cw1q4_interfaces__srv__detail__quat_to_rodrigues__rosidl_typesupport_introspection_c__QuatToRodrigues_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)cw1q4_interfaces__srv__detail__quat_to_rodrigues__rosidl_typesupport_introspection_c__QuatToRodrigues_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, cw1q4_interfaces, srv, QuatToRodrigues_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, cw1q4_interfaces, srv, QuatToRodrigues_Response)()->data;
  }

  return &cw1q4_interfaces__srv__detail__quat_to_rodrigues__rosidl_typesupport_introspection_c__QuatToRodrigues_service_type_support_handle;
}
