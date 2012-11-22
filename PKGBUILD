# Contributor : Devaev Maxim <mdevaev@gmail.com>

pkgname=python2-slib-git
pkgver=20121122
pkgrel=2
pkgdesc="Silverna library - a set of macros and fcgi-application to generate HTML pages"
arch=('any')
url="https://github.com/mdevaev/slib"
license="GPLv3"
depends=('python2-sourcelib-git' 'python2-cjson' 'python2-bencode' 'python2-decorator' 'python2-flup')
makedepends=('git' 'python2-distribute')
source=()
md5sums=()

_gitroot="git://github.com/mdevaev/slib.git"
_gitname="slib"


build() {
	cd $startdir/src
	if [ -d $_gitname ]; then
		msg "Updateing local repository..."
		cd $_gitname
		git pull origin master || return 1
		msg "The local files are updated."
		cd ..
	else
		git clone $_gitroot --depth=1
	fi

	msg "Git clone done or server timeout"
	msg "Starting make..."

	rm -rf $_gitname-build
	cp -r $_gitname $_gitname-build
	cd $_gitname-build

	python2 setup.py install --root="$pkgdir" --prefix=/usr
}

