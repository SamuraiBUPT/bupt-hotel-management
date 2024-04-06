# 指定版本
cmake_minimum_required(VERSION 3.24)
# 项目名
project(test)
# 引入外部依赖包
# include_directories(./crow/amaigamate)
include_directories(${CMAKE_CURRENT_SOURCE_DIR})

# 使用指定源文件来生成目标可执行文件
add_executable(main  crow_all.h main.cc)

target_link_libraries(main pthread)