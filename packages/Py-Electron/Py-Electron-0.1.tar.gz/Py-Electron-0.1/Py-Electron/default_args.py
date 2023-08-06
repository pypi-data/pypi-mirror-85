def get_args():
    arg_array = [
        "--proactive-tab-freeze-and-discard",
        "--ignore-gpu-blocklist",
        "--enable-lazy-image-loading",
        "--native-file-system-api",
        "--smooth-scrolling",
        "--disable-accelerated-2d-canvas",
        "--enable-quic",
        '--disable-dev-shm-usage',
        '--disable-extensions',
        '--disable-translate',
        '--metrics-recording-only',
        '--no-first-run',
        '--safebrowsing-disable-auto-update',
        '--enable-automation',
        '--autofill-api-key',
        '--autofill-metadata-upload-encoding',
        '--blink-settings',
        '--block-new-web-contents',
        '--browser-test',
        '--cast-initial-screen-height',
        '--cc-layer-tree-test-long-timeout',
        '--check-damage-early',
        '--component-updater',
        '--custom-launcher-page'
    ]
    return arg_array

def transform_args(window, arg_list):
    if window.dark_mode:
        arg_list.append("--enable-force-dark")

    arg_list.append(f"--window-size={str(window.height)}, {str(window.width)}")

    return arg_list
