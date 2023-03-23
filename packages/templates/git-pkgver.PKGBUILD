# SPDX-License-Identifier: CC0-1.0
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

pkgver() {
	if [ "x$GIT_REPO_DIR" = "x" ]; then
		pushd "$pkgname" >/dev/null
	else
		pushd "$GIT_REPO_DIR" >/dev/null
	fi
	printf "%s.r%s.%s" "$_pkgver" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
	popd >/dev/null
}
