
#include "global.h"
#include "ov.h"

FS_archive sdmcArchive = { 0x9, (FS_path){ PATH_EMPTY, 1, (u8*)"" } };
Handle fsUserHandle = 0;

#define CALLBACK_OVERLAY (101)

/*
Overlay Callback.
isBottom: 1 for bottom screen, 0 for top screen.
addr: writable cached framebuffer virtual address.
addrB: right-eye framebuffer for top screen, undefined for bottom screen.
stride: framebuffer stride(pitch) in bytes, at least 240*bytes_per_pixel.
format: framebuffer format, see https://www.3dbrew.org/wiki/GPU/External_Registers for details.

NTR will invalidate data cache of the framebuffer before calling overlay callbacks.
NTR will flush data cache after the callbacks were called and at least one overlay callback returns zero.

return 0 when the framebuffer was modified. return 1 when nothing in the framebuffer was modified.
*/

u32 overlayCallback(u32 isBottom, u32 addr, u32 addrB, u32 stride, u32 format) {

	char buf[40];
	int height = 12;
	int width  = 260;
	int level  = 1;
	int top = 9;
	int left = 14;

	xsprintf(buf, "HELLO WORLD | SCREEN ID --> [%d]", isBottom);

	ovDrawTranspartBlackRect(addr, stride, format, top, left, height, width, level);
	ovDrawString(addr, stride, format, sizeof(buf)*8, top+2, left+4, 255, 255, 255, buf);

	return 0;
}

int main() {
	initSharedFunc();
	plgRegisterCallback(CALLBACK_OVERLAY, (void*) overlayCallback, 0);
	return 0;
}

