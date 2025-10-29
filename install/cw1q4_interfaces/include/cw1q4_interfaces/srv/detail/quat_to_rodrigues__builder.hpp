// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from cw1q4_interfaces:srv/QuatToRodrigues.idl
// generated code does not contain a copyright notice

#ifndef CW1Q4_INTERFACES__SRV__DETAIL__QUAT_TO_RODRIGUES__BUILDER_HPP_
#define CW1Q4_INTERFACES__SRV__DETAIL__QUAT_TO_RODRIGUES__BUILDER_HPP_

#include "cw1q4_interfaces/srv/detail/quat_to_rodrigues__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace cw1q4_interfaces
{

namespace srv
{

namespace builder
{

class Init_QuatToRodrigues_Request_q
{
public:
  Init_QuatToRodrigues_Request_q()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::cw1q4_interfaces::srv::QuatToRodrigues_Request q(::cw1q4_interfaces::srv::QuatToRodrigues_Request::_q_type arg)
  {
    msg_.q = std::move(arg);
    return std::move(msg_);
  }

private:
  ::cw1q4_interfaces::srv::QuatToRodrigues_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::cw1q4_interfaces::srv::QuatToRodrigues_Request>()
{
  return cw1q4_interfaces::srv::builder::Init_QuatToRodrigues_Request_q();
}

}  // namespace cw1q4_interfaces


namespace cw1q4_interfaces
{

namespace srv
{

namespace builder
{

class Init_QuatToRodrigues_Response_z
{
public:
  explicit Init_QuatToRodrigues_Response_z(::cw1q4_interfaces::srv::QuatToRodrigues_Response & msg)
  : msg_(msg)
  {}
  ::cw1q4_interfaces::srv::QuatToRodrigues_Response z(::cw1q4_interfaces::srv::QuatToRodrigues_Response::_z_type arg)
  {
    msg_.z = std::move(arg);
    return std::move(msg_);
  }

private:
  ::cw1q4_interfaces::srv::QuatToRodrigues_Response msg_;
};

class Init_QuatToRodrigues_Response_y
{
public:
  explicit Init_QuatToRodrigues_Response_y(::cw1q4_interfaces::srv::QuatToRodrigues_Response & msg)
  : msg_(msg)
  {}
  Init_QuatToRodrigues_Response_z y(::cw1q4_interfaces::srv::QuatToRodrigues_Response::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_QuatToRodrigues_Response_z(msg_);
  }

private:
  ::cw1q4_interfaces::srv::QuatToRodrigues_Response msg_;
};

class Init_QuatToRodrigues_Response_x
{
public:
  Init_QuatToRodrigues_Response_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_QuatToRodrigues_Response_y x(::cw1q4_interfaces::srv::QuatToRodrigues_Response::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_QuatToRodrigues_Response_y(msg_);
  }

private:
  ::cw1q4_interfaces::srv::QuatToRodrigues_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::cw1q4_interfaces::srv::QuatToRodrigues_Response>()
{
  return cw1q4_interfaces::srv::builder::Init_QuatToRodrigues_Response_x();
}

}  // namespace cw1q4_interfaces

#endif  // CW1Q4_INTERFACES__SRV__DETAIL__QUAT_TO_RODRIGUES__BUILDER_HPP_
