// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from cw1q4_interfaces:srv/QuatToEuler.idl
// generated code does not contain a copyright notice

#ifndef CW1Q4_INTERFACES__SRV__DETAIL__QUAT_TO_EULER__STRUCT_HPP_
#define CW1Q4_INTERFACES__SRV__DETAIL__QUAT_TO_EULER__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


// Include directives for member types
// Member 'q'
#include "geometry_msgs/msg/detail/quaternion__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__cw1q4_interfaces__srv__QuatToEuler_Request __attribute__((deprecated))
#else
# define DEPRECATED__cw1q4_interfaces__srv__QuatToEuler_Request __declspec(deprecated)
#endif

namespace cw1q4_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct QuatToEuler_Request_
{
  using Type = QuatToEuler_Request_<ContainerAllocator>;

  explicit QuatToEuler_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : q(_init)
  {
    (void)_init;
  }

  explicit QuatToEuler_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : q(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _q_type =
    geometry_msgs::msg::Quaternion_<ContainerAllocator>;
  _q_type q;

  // setters for named parameter idiom
  Type & set__q(
    const geometry_msgs::msg::Quaternion_<ContainerAllocator> & _arg)
  {
    this->q = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    cw1q4_interfaces::srv::QuatToEuler_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const cw1q4_interfaces::srv::QuatToEuler_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<cw1q4_interfaces::srv::QuatToEuler_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<cw1q4_interfaces::srv::QuatToEuler_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      cw1q4_interfaces::srv::QuatToEuler_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<cw1q4_interfaces::srv::QuatToEuler_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      cw1q4_interfaces::srv::QuatToEuler_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<cw1q4_interfaces::srv::QuatToEuler_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<cw1q4_interfaces::srv::QuatToEuler_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<cw1q4_interfaces::srv::QuatToEuler_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__cw1q4_interfaces__srv__QuatToEuler_Request
    std::shared_ptr<cw1q4_interfaces::srv::QuatToEuler_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__cw1q4_interfaces__srv__QuatToEuler_Request
    std::shared_ptr<cw1q4_interfaces::srv::QuatToEuler_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const QuatToEuler_Request_ & other) const
  {
    if (this->q != other.q) {
      return false;
    }
    return true;
  }
  bool operator!=(const QuatToEuler_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct QuatToEuler_Request_

// alias to use template instance with default allocator
using QuatToEuler_Request =
  cw1q4_interfaces::srv::QuatToEuler_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace cw1q4_interfaces


// Include directives for member types
// Member 'z'
// Member 'y'
// Member 'x'
#include "std_msgs/msg/detail/float64__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__cw1q4_interfaces__srv__QuatToEuler_Response __attribute__((deprecated))
#else
# define DEPRECATED__cw1q4_interfaces__srv__QuatToEuler_Response __declspec(deprecated)
#endif

namespace cw1q4_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct QuatToEuler_Response_
{
  using Type = QuatToEuler_Response_<ContainerAllocator>;

  explicit QuatToEuler_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : z(_init),
    y(_init),
    x(_init)
  {
    (void)_init;
  }

  explicit QuatToEuler_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : z(_alloc, _init),
    y(_alloc, _init),
    x(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _z_type =
    std_msgs::msg::Float64_<ContainerAllocator>;
  _z_type z;
  using _y_type =
    std_msgs::msg::Float64_<ContainerAllocator>;
  _y_type y;
  using _x_type =
    std_msgs::msg::Float64_<ContainerAllocator>;
  _x_type x;

  // setters for named parameter idiom
  Type & set__z(
    const std_msgs::msg::Float64_<ContainerAllocator> & _arg)
  {
    this->z = _arg;
    return *this;
  }
  Type & set__y(
    const std_msgs::msg::Float64_<ContainerAllocator> & _arg)
  {
    this->y = _arg;
    return *this;
  }
  Type & set__x(
    const std_msgs::msg::Float64_<ContainerAllocator> & _arg)
  {
    this->x = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    cw1q4_interfaces::srv::QuatToEuler_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const cw1q4_interfaces::srv::QuatToEuler_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<cw1q4_interfaces::srv::QuatToEuler_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<cw1q4_interfaces::srv::QuatToEuler_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      cw1q4_interfaces::srv::QuatToEuler_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<cw1q4_interfaces::srv::QuatToEuler_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      cw1q4_interfaces::srv::QuatToEuler_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<cw1q4_interfaces::srv::QuatToEuler_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<cw1q4_interfaces::srv::QuatToEuler_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<cw1q4_interfaces::srv::QuatToEuler_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__cw1q4_interfaces__srv__QuatToEuler_Response
    std::shared_ptr<cw1q4_interfaces::srv::QuatToEuler_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__cw1q4_interfaces__srv__QuatToEuler_Response
    std::shared_ptr<cw1q4_interfaces::srv::QuatToEuler_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const QuatToEuler_Response_ & other) const
  {
    if (this->z != other.z) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    if (this->x != other.x) {
      return false;
    }
    return true;
  }
  bool operator!=(const QuatToEuler_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct QuatToEuler_Response_

// alias to use template instance with default allocator
using QuatToEuler_Response =
  cw1q4_interfaces::srv::QuatToEuler_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace cw1q4_interfaces

namespace cw1q4_interfaces
{

namespace srv
{

struct QuatToEuler
{
  using Request = cw1q4_interfaces::srv::QuatToEuler_Request;
  using Response = cw1q4_interfaces::srv::QuatToEuler_Response;
};

}  // namespace srv

}  // namespace cw1q4_interfaces

#endif  // CW1Q4_INTERFACES__SRV__DETAIL__QUAT_TO_EULER__STRUCT_HPP_
