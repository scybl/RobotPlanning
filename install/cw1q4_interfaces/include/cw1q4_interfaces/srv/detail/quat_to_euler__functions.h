// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from cw1q4_interfaces:srv/QuatToEuler.idl
// generated code does not contain a copyright notice

#ifndef CW1Q4_INTERFACES__SRV__DETAIL__QUAT_TO_EULER__FUNCTIONS_H_
#define CW1Q4_INTERFACES__SRV__DETAIL__QUAT_TO_EULER__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "cw1q4_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "cw1q4_interfaces/srv/detail/quat_to_euler__struct.h"

/// Initialize srv/QuatToEuler message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * cw1q4_interfaces__srv__QuatToEuler_Request
 * )) before or use
 * cw1q4_interfaces__srv__QuatToEuler_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_cw1q4_interfaces
bool
cw1q4_interfaces__srv__QuatToEuler_Request__init(cw1q4_interfaces__srv__QuatToEuler_Request * msg);

/// Finalize srv/QuatToEuler message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_cw1q4_interfaces
void
cw1q4_interfaces__srv__QuatToEuler_Request__fini(cw1q4_interfaces__srv__QuatToEuler_Request * msg);

/// Create srv/QuatToEuler message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * cw1q4_interfaces__srv__QuatToEuler_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_cw1q4_interfaces
cw1q4_interfaces__srv__QuatToEuler_Request *
cw1q4_interfaces__srv__QuatToEuler_Request__create();

/// Destroy srv/QuatToEuler message.
/**
 * It calls
 * cw1q4_interfaces__srv__QuatToEuler_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_cw1q4_interfaces
void
cw1q4_interfaces__srv__QuatToEuler_Request__destroy(cw1q4_interfaces__srv__QuatToEuler_Request * msg);

/// Check for srv/QuatToEuler message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_cw1q4_interfaces
bool
cw1q4_interfaces__srv__QuatToEuler_Request__are_equal(const cw1q4_interfaces__srv__QuatToEuler_Request * lhs, const cw1q4_interfaces__srv__QuatToEuler_Request * rhs);

/// Copy a srv/QuatToEuler message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_cw1q4_interfaces
bool
cw1q4_interfaces__srv__QuatToEuler_Request__copy(
  const cw1q4_interfaces__srv__QuatToEuler_Request * input,
  cw1q4_interfaces__srv__QuatToEuler_Request * output);

/// Initialize array of srv/QuatToEuler messages.
/**
 * It allocates the memory for the number of elements and calls
 * cw1q4_interfaces__srv__QuatToEuler_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_cw1q4_interfaces
bool
cw1q4_interfaces__srv__QuatToEuler_Request__Sequence__init(cw1q4_interfaces__srv__QuatToEuler_Request__Sequence * array, size_t size);

/// Finalize array of srv/QuatToEuler messages.
/**
 * It calls
 * cw1q4_interfaces__srv__QuatToEuler_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_cw1q4_interfaces
void
cw1q4_interfaces__srv__QuatToEuler_Request__Sequence__fini(cw1q4_interfaces__srv__QuatToEuler_Request__Sequence * array);

/// Create array of srv/QuatToEuler messages.
/**
 * It allocates the memory for the array and calls
 * cw1q4_interfaces__srv__QuatToEuler_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_cw1q4_interfaces
cw1q4_interfaces__srv__QuatToEuler_Request__Sequence *
cw1q4_interfaces__srv__QuatToEuler_Request__Sequence__create(size_t size);

/// Destroy array of srv/QuatToEuler messages.
/**
 * It calls
 * cw1q4_interfaces__srv__QuatToEuler_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_cw1q4_interfaces
void
cw1q4_interfaces__srv__QuatToEuler_Request__Sequence__destroy(cw1q4_interfaces__srv__QuatToEuler_Request__Sequence * array);

/// Check for srv/QuatToEuler message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_cw1q4_interfaces
bool
cw1q4_interfaces__srv__QuatToEuler_Request__Sequence__are_equal(const cw1q4_interfaces__srv__QuatToEuler_Request__Sequence * lhs, const cw1q4_interfaces__srv__QuatToEuler_Request__Sequence * rhs);

/// Copy an array of srv/QuatToEuler messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_cw1q4_interfaces
bool
cw1q4_interfaces__srv__QuatToEuler_Request__Sequence__copy(
  const cw1q4_interfaces__srv__QuatToEuler_Request__Sequence * input,
  cw1q4_interfaces__srv__QuatToEuler_Request__Sequence * output);

/// Initialize srv/QuatToEuler message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * cw1q4_interfaces__srv__QuatToEuler_Response
 * )) before or use
 * cw1q4_interfaces__srv__QuatToEuler_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_cw1q4_interfaces
bool
cw1q4_interfaces__srv__QuatToEuler_Response__init(cw1q4_interfaces__srv__QuatToEuler_Response * msg);

/// Finalize srv/QuatToEuler message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_cw1q4_interfaces
void
cw1q4_interfaces__srv__QuatToEuler_Response__fini(cw1q4_interfaces__srv__QuatToEuler_Response * msg);

/// Create srv/QuatToEuler message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * cw1q4_interfaces__srv__QuatToEuler_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_cw1q4_interfaces
cw1q4_interfaces__srv__QuatToEuler_Response *
cw1q4_interfaces__srv__QuatToEuler_Response__create();

/// Destroy srv/QuatToEuler message.
/**
 * It calls
 * cw1q4_interfaces__srv__QuatToEuler_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_cw1q4_interfaces
void
cw1q4_interfaces__srv__QuatToEuler_Response__destroy(cw1q4_interfaces__srv__QuatToEuler_Response * msg);

/// Check for srv/QuatToEuler message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_cw1q4_interfaces
bool
cw1q4_interfaces__srv__QuatToEuler_Response__are_equal(const cw1q4_interfaces__srv__QuatToEuler_Response * lhs, const cw1q4_interfaces__srv__QuatToEuler_Response * rhs);

/// Copy a srv/QuatToEuler message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_cw1q4_interfaces
bool
cw1q4_interfaces__srv__QuatToEuler_Response__copy(
  const cw1q4_interfaces__srv__QuatToEuler_Response * input,
  cw1q4_interfaces__srv__QuatToEuler_Response * output);

/// Initialize array of srv/QuatToEuler messages.
/**
 * It allocates the memory for the number of elements and calls
 * cw1q4_interfaces__srv__QuatToEuler_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_cw1q4_interfaces
bool
cw1q4_interfaces__srv__QuatToEuler_Response__Sequence__init(cw1q4_interfaces__srv__QuatToEuler_Response__Sequence * array, size_t size);

/// Finalize array of srv/QuatToEuler messages.
/**
 * It calls
 * cw1q4_interfaces__srv__QuatToEuler_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_cw1q4_interfaces
void
cw1q4_interfaces__srv__QuatToEuler_Response__Sequence__fini(cw1q4_interfaces__srv__QuatToEuler_Response__Sequence * array);

/// Create array of srv/QuatToEuler messages.
/**
 * It allocates the memory for the array and calls
 * cw1q4_interfaces__srv__QuatToEuler_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_cw1q4_interfaces
cw1q4_interfaces__srv__QuatToEuler_Response__Sequence *
cw1q4_interfaces__srv__QuatToEuler_Response__Sequence__create(size_t size);

/// Destroy array of srv/QuatToEuler messages.
/**
 * It calls
 * cw1q4_interfaces__srv__QuatToEuler_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_cw1q4_interfaces
void
cw1q4_interfaces__srv__QuatToEuler_Response__Sequence__destroy(cw1q4_interfaces__srv__QuatToEuler_Response__Sequence * array);

/// Check for srv/QuatToEuler message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_cw1q4_interfaces
bool
cw1q4_interfaces__srv__QuatToEuler_Response__Sequence__are_equal(const cw1q4_interfaces__srv__QuatToEuler_Response__Sequence * lhs, const cw1q4_interfaces__srv__QuatToEuler_Response__Sequence * rhs);

/// Copy an array of srv/QuatToEuler messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_cw1q4_interfaces
bool
cw1q4_interfaces__srv__QuatToEuler_Response__Sequence__copy(
  const cw1q4_interfaces__srv__QuatToEuler_Response__Sequence * input,
  cw1q4_interfaces__srv__QuatToEuler_Response__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // CW1Q4_INTERFACES__SRV__DETAIL__QUAT_TO_EULER__FUNCTIONS_H_
