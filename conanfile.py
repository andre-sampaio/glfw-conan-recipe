from conans import ConanFile, CMake, tools
import os

class GlfwConan(ConanFile):
    name = "glfw"
    version = "3.2.1"
    license = "BDS"
    url = ""
    description = "Glfw"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/glfw/glfw.git")
        self.run("cd glfw && git fetch --all --tags --prune")
        self.run("cd glfw && git checkout tags/3.2.1 -b release/3.2.1")
        
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file(os.path.join('glfw', 'CMakeLists.txt'), "project(GLFW C)",
                              '''project(GLFW C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder='glfw', defs={"GLFW_BUILD_EXAMPLES": False, "GLFW_BUILD_TESTS": False, "GLFW_BUILD_DOCS":False})
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src=os.path.join('glfw', 'include'))
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["glfw3"]

