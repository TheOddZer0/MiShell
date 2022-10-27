OBJCOPY       :=llvm-objcopy
OBJCOPY_FLAGS :=

CLANG         :=clang
PAYLOAD_FLAGS :=-x assembler-with-cpp -nostdlib -nostdinc
CLANG_FLAGS   :=-Wall -Wextra -fno-stack-protector -z execstack