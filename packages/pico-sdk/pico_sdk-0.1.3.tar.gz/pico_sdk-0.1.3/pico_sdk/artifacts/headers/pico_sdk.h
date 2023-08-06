#include <stdarg.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>

/**
 * Streaming data callback signature
 *
 * `channel_names` - Comma separated list of channel names
 * `samples` - A pointer to a continuous block containing all channel data.
 *      Channels are laid out in order of `channel_names`
 * `num_samples_per_ch` - The number of samples per channel. `samples` length
 *      is equal to `num_samples_per_ch` multiplied by the number of channels
 */
typedef void (*DataCallback)(const char *channel_names, const float *samples, uint32_t num_samples_per_ch);

/**
 * # Disables a channel
 */
bool device_disable_channel(PicoDevice *device_ptr, const char *channel);

/**
 * # Enables a channel
 *
 * Enables and channel and sets its configuration
 */
bool device_enable_channel(PicoDevice *device_ptr,
                           const char *channel,
                           const char *range,
                           const char *coupling);

/**
 * # Frees a device
 */
void device_free(PicoDevice *device_ptr);

/**
 * # Gets the supported ranges for a channel
 *
 * If a non-null pointer is returned, ensure it is passed to `string_free`
 * so that the memory can be freed
 */
char *device_get_channel_ranges(PicoDevice *device_ptr, const char *channel);

/**
 * # Gets the devices serial string
 *
 * If a non-null pointer is returned, ensure it is passed to `string_free`
 * so that the memory can be freed
 */
char *device_get_serial(PicoDevice *device_ptr);

/**
 * # Gets the devices variant
 *
 * If a non-null pointer is returned, ensure it is passed to `string_free`
 * so that the memory can be freed
 */
char *device_get_variant(PicoDevice *device_ptr);

/**
 * # Opens a device
 * `serial` - Optional serial of device to be opened
 * `download_missing_drivers` - Whether to download drivers if they are missing
 * `base_path` - Optional path to attempt to load drivers from
 */
PicoDevice *device_open(const char *serial, bool download_missing_drivers);

/**
 * # Sets the streaming data callback
 */
bool device_set_callback(PicoDevice *device_ptr, DataCallback callback);

/**
 * # Starts streaming scaled values
 */
uint32_t device_start_streaming(PicoDevice *device_ptr, uint32_t samples_per_second);

/**
 * # Starts streaming scaled values
 */
bool device_stop_streaming(PicoDevice *device_ptr);

/**
 * # Lists available devices
 *
 * If a non-null pointer is returned, ensure it is passed to `string_free`
 * so that the memory can be freed
 */
char *enumerate_devices(bool download_missing_drivers);

/**
 * Fetches a pointer to a string detailing the last encountered error
 * Returns a null pointer if no error was found
 *
 * If a non-null pointer is returned, ensure it is passed to `string_free`
 * so that the memory can be freed
 */
char *last_error(void);

/**
 * Frees string pointer returned from other methods
 */
void string_free(char *str_ptr);
