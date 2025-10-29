// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from cw1q4_interfaces:srv/QuatToRodrigues.idl
// generated code does not contain a copyright notice

#ifndef CW1Q4_INTERFACES__SRV__DETAIL__QUAT_TO_RODRIGUES__TRAITS_HPP_
#define CW1Q4_INTERFACES__SRV__DETAIL__QUAT_TO_RODRIGUES__TRAITS_HPP_

#include "cw1q4_interfaces/srv/detail/quat_to_rodrigues__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

// Include directives for member types
// Member 'q'
#include "geometry_msgs/msg/detail/quaternion__traits.hpp"

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<cw1q4_interfaces::srv::QuatToRodrigues_Request>()
{
  return "cw1q4_interfaces::srv::QuatToRodrigues_Request";
}

template<>
inline const char * name<cw1q4_interfaces::srv::QuatToRodrigues_Request>()
{
  return "cw1q4_interfaces/srv/QuatToRodrigues_Request";
}

template<>
struct has_fixed_size<cw1q4_interfaces::srv::QuatToRodrigues_Request>
  : std::integral_constant<bool, has_fixed_size<geometry_msgs::msg::Quaternion>::value> {};

template<>
struct has_bounded_size<cw1q4_interfaces::srv::QuatToRodrigues_Request>
  : std::integral_constant<bool, has_bounded_size<geometry_msgs::msg::Quaternion>::value> {};

template<>
struct is_message<cw1q4_interfaces::srv::QuatToRodrigues_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'x'
// Member 'y'
// Member 'z'
#include "std_msgs/msg/detail/float64__traits.hpp"

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<cw1q4_interfaces::srv::QuatToRodrigues_Response>()
{
  return "cw1q4_interfaces::srv::QuatToRodrigues_Response";
}

template<>
inline const char * name<cw1q4_interfaces::srv::QuatToRodrigues_Response>()
{
  return "cw1q4_interfaces/srv/QuatToRodrigues_Response";
}

template<>
struct has_fixed_size<cw1q4_interfaces::srv::QuatToRodrigues_Response>
  : std::integral_constant<bool, has_fixed_size<std_msgs::msg::Float64>::value> {};

template<>
struct has_bounded_size<cw1q4_interfaces::srv::QuatToRodrigues_Response>
  : std::integral_constant<bool, has_bounded_size<std_msgs::msg::Float64>::value> {};

template<>
struct is_message<cw1q4_interfaces::srv::QuatToRodrigues_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<cw1q4_interfaces::srv::QuatToRodrigues>()
{
  return "cw1q4_interfaces::srv::QuatToRodrigues";
}

template<>
inline const char * name<cw1q4_interfaces::srv::QuatToRodrigues>()
{
  return "cw1q4_interfaces/srv/QuatToRodrigues";
}

template<>
struct has_fixed_size<cw1q4_interfaces::srv::QuatToRodrigues>
  : std::integral_constant<
    bool,
    has_fixed_size<cw1q4_interfaces::srv::QuatToRodrigues_Request>::value &&
    has_fixed_size<cw1q4_interfaces::srv::QuatToRodrigues_Response>::value
  >
{
};

template<>
struct has_bounded_size<cw1q4_interfaces::srv::QuatToRodrigues>
  : std::integral_constant<
    bool,
    has_bounded_size<cw1q4_interfaces::srv::QuatToRodrigues_Request>::value &&
    has_bounded_size<cw1q4_interfaces::srv::QuatToRodrigues_Response>::value
  >
{
};

template<>
struct is_service<cw1q4_interfaces::srv::QuatToRodrigues>
  : std::true_type
{
};

template<>
struct is_service_request<cw1q4_interfaces::srv::QuatToRodrigues_Request>
  : std::true_type
{
};

template<>
struct is_service_response<cw1q4_interfaces::srv::QuatToRodrigues_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // CW1Q4_INTERFACES__SRV__DETAIL__QUAT_TO_RODRIGUES__TRAITS_HPP_
