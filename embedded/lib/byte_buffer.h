// FIXME: This is a temporary hack solution
namespace byte_buffer {
	unsigned char buffer[4];

	void from_u_int(unsigned int value) {
		buffer[0] = (unsigned char)((value >> 24) & 0xFF);
		buffer[1] = (unsigned char)((value >> 16) & 0xFF);
		buffer[2] = (unsigned char)((value >> 8) & 0xFF);
		buffer[3] = (unsigned char)(value & 0xFF);
	};
}
