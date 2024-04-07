# 指定版本
cmake_minimum_required(VERSION 3.24)

# 项目名
project(bupt-hotel-management)

# 使用协程
add_compile_options(-fcoroutines)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})

# 使用指定源文件来生成目标可执行文件
add_executable(main crow_all.h main.cc)

target_link_libraries(main pthread)