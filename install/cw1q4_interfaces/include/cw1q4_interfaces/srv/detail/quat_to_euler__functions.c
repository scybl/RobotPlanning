// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from cw1q4_interfaces:srv/QuatToEuler.idl
// generated code does not contain a copyright notice
#include "cw1q4_interfaces/srv/detail/quat_to_euler__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `q`
#include "geometry_msgs/msg/detail/quaternion__functions.h"

bool
cw1q4_interfaces__srv__QuatToEuler_Request__init(cw1q4_interfaces__srv__QuatToEuler_Request * msg)
{
  if (!msg) {
    return false;
  }
  // q
  if (!geometry_msgs__msg__Quaternion__init(&msg->q)) {
    cw1q4_interfaces__srv__QuatToEuler_Request__fini(msg);
    return false;
  }
  return true;
}

void
cw1q4_interfaces__srv__QuatToEuler_Request__fini(cw1q4_interfaces__srv__QuatToEuler_Request * msg)
{
  if (!msg) {
    return;
  }
  // q
  geometry_msgs__msg__Quaternion__fini(&msg->q);
}

bool
cw1q4_interfaces__srv__QuatToEuler_Request__are_equal(const cw1q4_interfaces__srv__QuatToEuler_Request * lhs, const cw1q4_interfaces__srv__QuatToEuler_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // q
  if (!geometry_msgs__msg__Quaternion__are_equal(
      &(lhs->q), &(rhs->q)))
  {
    return false;
  }
  return true;
}

bool
cw1q4_interfaces__srv__QuatToEuler_Request__copy(
  const cw1q4_interfaces__srv__QuatToEuler_Request * input,
  cw1q4_interfaces__srv__QuatToEuler_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // q
  if (!geometry_msgs__msg__Quaternion__copy(
      &(input->q), &(output->q)))
  {
    return false;
  }
  return true;
}

cw1q4_interfaces__srv__QuatToEuler_Request *
cw1q4_interfaces__srv__QuatToEuler_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  cw1q4_interfaces__srv__QuatToEuler_Request * msg = (cw1q4_interfaces__srv__QuatToEuler_Request *)allocator.allocate(sizeof(cw1q4_interfaces__srv__QuatToEuler_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(cw1q4_interfaces__srv__QuatToEuler_Request));
  bool success = cw1q4_interfaces__srv__QuatToEuler_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
cw1q4_interfaces__srv__QuatToEuler_Request__destroy(cw1q4_interfaces__srv__QuatToEuler_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    cw1q4_interfaces__srv__QuatToEuler_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
cw1q4_interfaces__srv__QuatToEuler_Request__Sequence__init(cw1q4_interfaces__srv__QuatToEuler_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  cw1q4_interfaces__srv__QuatToEuler_Request * data = NULL;

  if (size) {
    data = (cw1q4_interfaces__srv__QuatToEuler_Request *)allocator.zero_allocate(size, sizeof(cw1q4_interfaces__srv__QuatToEuler_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = cw1q4_interfaces__srv__QuatToEuler_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        cw1q4_interfaces__srv__QuatToEuler_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
cw1q4_interfaces__srv__QuatToEuler_Request__Sequence__fini(cw1q4_interfaces__srv__QuatToEuler_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      cw1q4_interfaces__srv__QuatToEuler_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

cw1q4_interfaces__srv__QuatToEuler_Request__Sequence *
cw1q4_interfaces__srv__QuatToEuler_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  cw1q4_interfaces__srv__QuatToEuler_Request__Sequence * array = (cw1q4_interfaces__srv__QuatToEuler_Request__Sequence *)allocator.allocate(sizeof(cw1q4_interfaces__srv__QuatToEuler_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = cw1q4_interfaces__srv__QuatToEuler_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
cw1q4_interfaces__srv__QuatToEuler_Request__Sequence__destroy(cw1q4_interfaces__srv__QuatToEuler_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    cw1q4_interfaces__srv__QuatToEuler_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
cw1q4_interfaces__srv__QuatToEuler_Request__Sequence__are_equal(const cw1q4_interfaces__srv__QuatToEuler_Request__Sequence * lhs, const cw1q4_interfaces__srv__QuatToEuler_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!cw1q4_interfaces__srv__QuatToEuler_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
cw1q4_interfaces__srv__QuatToEuler_Request__Sequence__copy(
  const cw1q4_interfaces__srv__QuatToEuler_Request__Sequence * input,
  cw1q4_interfaces__srv__QuatToEuler_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(cw1q4_interfaces__srv__QuatToEuler_Request);
    cw1q4_interfaces__srv__QuatToEuler_Request * data =
      (cw1q4_interfaces__srv__QuatToEuler_Request *)realloc(output->data, allocation_size);
    if (!data) {
      return false;
    }
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!cw1q4_interfaces__srv__QuatToEuler_Request__init(&data[i])) {
        /* free currently allocated and return false */
        for (; i-- > output->capacity; ) {
          cw1q4_interfaces__srv__QuatToEuler_Request__fini(&data[i]);
        }
        free(data);
        return false;
      }
    }
    output->data = data;
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!cw1q4_interfaces__srv__QuatToEuler_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `z`
// Member `y`
// Member `x`
#include "std_msgs/msg/detail/float64__functions.h"

bool
cw1q4_interfaces__srv__QuatToEuler_Response__init(cw1q4_interfaces__srv__QuatToEuler_Response * msg)
{
  if (!msg) {
    return false;
  }
  // z
  if (!std_msgs__msg__Float64__init(&msg->z)) {
    cw1q4_interfaces__srv__QuatToEuler_Response__fini(msg);
    return false;
  }
  // y
  if (!std_msgs__msg__Float64__init(&msg->y)) {
    cw1q4_interfaces__srv__QuatToEuler_Response__fini(msg);
    return false;
  }
  // x
  if (!std_msgs__msg__Float64__init(&msg->x)) {
    cw1q4_interfaces__srv__QuatToEuler_Response__fini(msg);
    return false;
  }
  return true;
}

void
cw1q4_interfaces__srv__QuatToEuler_Response__fini(cw1q4_interfaces__srv__QuatToEuler_Response * msg)
{
  if (!msg) {
    return;
  }
  // z
  std_msgs__msg__Float64__fini(&msg->z);
  // y
  std_msgs__msg__Float64__fini(&msg->y);
  // x
  std_msgs__msg__Float64__fini(&msg->x);
}

bool
cw1q4_interfaces__srv__QuatToEuler_Response__are_equal(const cw1q4_interfaces__srv__QuatToEuler_Response * lhs, const cw1q4_interfaces__srv__QuatToEuler_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // z
  if (!std_msgs__msg__Float64__are_equal(
      &(lhs->z), &(rhs->z)))
  {
    return false;
  }
  // y
  if (!std_msgs__msg__Float64__are_equal(
      &(lhs->y), &(rhs->y)))
  {
    return false;
  }
  // x
  if (!std_msgs__msg__Float64__are_equal(
      &(lhs->x), &(rhs->x)))
  {
    return false;
  }
  return true;
}

bool
cw1q4_interfaces__srv__QuatToEuler_Response__copy(
  const cw1q4_interfaces__srv__QuatToEuler_Response * input,
  cw1q4_interfaces__srv__QuatToEuler_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // z
  if (!std_msgs__msg__Float64__copy(
      &(input->z), &(output->z)))
  {
    return false;
  }
  // y
  if (!std_msgs__msg__Float64__copy(
      &(input->y), &(output->y)))
  {
    return false;
  }
  // x
  if (!std_msgs__msg__Float64__copy(
      &(input->x), &(output->x)))
  {
    return false;
  }
  return true;
}

cw1q4_interfaces__srv__QuatToEuler_Response *
cw1q4_interfaces__srv__QuatToEuler_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  cw1q4_interfaces__srv__QuatToEuler_Response * msg = (cw1q4_interfaces__srv__QuatToEuler_Response *)allocator.allocate(sizeof(cw1q4_interfaces__srv__QuatToEuler_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(cw1q4_interfaces__srv__QuatToEuler_Response));
  bool success = cw1q4_interfaces__srv__QuatToEuler_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
cw1q4_interfaces__srv__QuatToEuler_Response__destroy(cw1q4_interfaces__srv__QuatToEuler_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    cw1q4_interfaces__srv__QuatToEuler_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
cw1q4_interfaces__srv__QuatToEuler_Response__Sequence__init(cw1q4_interfaces__srv__QuatToEuler_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  cw1q4_interfaces__srv__QuatToEuler_Response * data = NULL;

  if (size) {
    data = (cw1q4_interfaces__srv__QuatToEuler_Response *)allocator.zero_allocate(size, sizeof(cw1q4_interfaces__srv__QuatToEuler_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = cw1q4_interfaces__srv__QuatToEuler_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        cw1q4_interfaces__srv__QuatToEuler_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
cw1q4_interfaces__srv__QuatToEuler_Response__Sequence__fini(cw1q4_interfaces__srv__QuatToEuler_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      cw1q4_interfaces__srv__QuatToEuler_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

cw1q4_interfaces__srv__QuatToEuler_Response__Sequence *
cw1q4_interfaces__srv__QuatToEuler_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  cw1q4_interfaces__srv__QuatToEuler_Response__Sequence * array = (cw1q4_interfaces__srv__QuatToEuler_Response__Sequence *)allocator.allocate(sizeof(cw1q4_interfaces__srv__QuatToEuler_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = cw1q4_interfaces__srv__QuatToEuler_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
cw1q4_interfaces__srv__QuatToEuler_Response__Sequence__destroy(cw1q4_interfaces__srv__QuatToEuler_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    cw1q4_interfaces__srv__QuatToEuler_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
cw1q4_interfaces__srv__QuatToEuler_Response__Sequence__are_equal(const cw1q4_interfaces__srv__QuatToEuler_Response__Sequence * lhs, const cw1q4_interfaces__srv__QuatToEuler_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!cw1q4_interfaces__srv__QuatToEuler_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
cw1q4_interfaces__srv__QuatToEuler_Response__Sequence__copy(
  const cw1q4_interfaces__srv__QuatToEuler_Response__Sequence * input,
  cw1q4_interfaces__srv__QuatToEuler_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(cw1q4_interfaces__srv__QuatToEuler_Response);
    cw1q4_interfaces__srv__QuatToEuler_Response * data =
      (cw1q4_interfaces__srv__QuatToEuler_Response *)realloc(output->data, allocation_size);
    if (!data) {
      return false;
    }
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!cw1q4_interfaces__srv__QuatToEuler_Response__init(&data[i])) {
        /* free currently allocated and return false */
        for (; i-- > output->capacity; ) {
          cw1q4_interfaces__srv__QuatToEuler_Response__fini(&data[i]);
        }
        free(data);
        return false;
      }
    }
    output->data = data;
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!cw1q4_interfaces__srv__QuatToEuler_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
