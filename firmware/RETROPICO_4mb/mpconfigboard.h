// Board and hardware specific configuration
#define MICROPY_HW_BOARD_NAME                   "RetroPico V1.x 4MB"

// Annule la définition système par défaut
#undef MICROPY_HW_FLASH_STORAGE_BYTES

// configuration pour le flash de 4mb
#define MICROPY_HW_FLASH_STORAGE_BYTES (3584 * 1024)
