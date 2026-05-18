cmake_minimum_required(VERSION 3.5)
project(my_robot_description)

# 找到必要的包
find_package(ament_cmake REQUIRED)
find_package(xacro REQUIRED)

# 安装 urdf 目录
install(DIRECTORY urdf
  DESTINATION share/${PROJECT_NAME}
)

# 安装 launch 目录
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

# ament 包配置
ament_package()





