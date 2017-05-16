from conans import ConanFile, CMake, tools
import os, shutil


class HelloConan(ConanFile):
    name = "Hello"
    version = "0.1"
    settings = "os", "compiler", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports_sources = "hello/*"

    def build(self):
        cmake = CMake(self)
        if cmake.is_multi_configuration:
            cmd = 'cmake "%s/hello" %s' % (self.conanfile_directory, cmake.command_line)
            self.run(cmd)
            self.run("cmake --build . --config Debug")
            self.run("cmake --build . --config Release")
        else:
            for config in ("Debug", "Release"):
                self.output.info("Building %s" % config)
                self.run('cmake "%s/hello" %s -DCMAKE_BUILD_TYPE=%s'
                        % (self.conanfile_directory, cmake.command_line, config))
                self.run("cmake --build .")
                shutil.rmtree("CMakeFiles")
                os.remove("CMakeCache.txt")

    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.release.libs = ["hello"]
        self.cpp_info.debug.libs = ["hello_d"]
