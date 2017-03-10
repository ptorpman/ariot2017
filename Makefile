SRC_C = clouduploader.c
OBJ   = $(SRC_C:.c=.o)


all: clouduploader

clouduploader: $(OBJ)

%.o: %.c
	$(CC) -c $^ -o $@
