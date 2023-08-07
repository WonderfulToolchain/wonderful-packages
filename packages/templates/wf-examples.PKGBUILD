# SPDX-License-Identifier: CC0-1.0
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

build() {
	cd "$pkgname"
}

package() {
	cd "$pkgname"
	mkdir -p "$pkgdir$WF_DESTDIR"
	if [ -d templates ]; then
		cp -aR templates "$pkgdir$WF_DESTDIR"
	fi
	if [ -d examples ]; then
		mkdir -p "$pkgdir$WF_DESTDIR"/examples/"$target"
		cp -aR examples/* "$pkgdir$WF_DESTDIR"/examples/"$target"/
	fi
}
