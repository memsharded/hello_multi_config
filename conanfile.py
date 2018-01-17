from conans import ConanFile, CMake
import os, shutil


class HelloConan(ConanFile):
    name = "Hello"
    version = "0.1"
    settings = "os", "compiler", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports_sources = "hello/*"

    # Alternative 1: remove runtime, use always default (MD/MDd)
    def configure(self):
        if self.settings.compiler == "Visual Studio":
            del self.settings.compiler.runtime

    # Alternative 2: if you want to keep MD-MDd/MT-MTd configuration
    # def package_id(self):
    #     if self.settings.compiler == "Visual Studio":
    #         if "MD" in self.settings.compiler.runtime:
    #             self.info.settings.compiler.runtime = "MD/MDd"
    #         else:
    #             self.info.settings.compiler.runtime = "MT/MTd"

    def build(self):
        cmake = CMake(self)
        if cmake.is_multi_configuration:
            # Alternative 1:
            cmd_args = cmake.command_line
            # Alternative 2:
            # cmd_args = cmake.command_line.replace("CONAN_LINK_RUNTIME", "CONAN_LINK_RUNTIME_MULTI")
            cmd = 'cmake "%s/hello" %s' % (self.source_folder, cmd_args)
            self.run(cmd)
            self.run("cmake --build . --config Debug")
            self.run("cmake --build . --config Release")
        else:
            for config in ("Debug", "Release"):
                self.output.info("Building %s" % config)
                self.run('cmake "%s/hello" %s -DCMAKE_BUILD_TYPE=%s'
                        % (self.source_folder, cmake.command_line, config))
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
