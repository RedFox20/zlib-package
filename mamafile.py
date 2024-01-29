import mama
from mama.utils.system import console
from mama.utils.gnu_project import BuildProduct

# Explore Mama docs at https://github.com/RedFox20/Mama
class zlib(mama.BuildTarget):

    local_workspace = 'packages'

    def init(self):
        self.zlib = self.gnu_project('zlib', '1.3.1',
            url='http://kratt.codefox.ee/linux/{{project}}.tar.gz',
            build_products=[
                BuildProduct('{{installed}}/lib/libz.a', None),
            ])

    def settings(self):
        self.config.prefer_gcc(self.name)
        if self.mips:
            self.config.set_mips_toolchain('mipsel')

    def build(self):
        if self.zlib.should_build():
            # override to always run configure
            self.zlib.configure_command = f'configure --static --prefix {self.zlib.install_dir()}'
            self.zlib.extra_env['CFLAGS'] = '-fPIC'
            self.zlib.build()
        else:
            console('lib/libz.a already built', color='green')

    def package(self):
        self.export_include('zlib-built/include', build_dir=True)
        self.export_lib('zlib-built/lib/libz.a', build_dir=True)
