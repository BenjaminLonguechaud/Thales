"""
Tkinter UI Styles and Configuration
Centralized styling parameters for the CRDP Data Protection application.
Customize colors, fonts, dimensions, and padding here without modifying application logic.
"""

# ============================================================================
# COLORS
# ============================================================================

# Window and background colors
WINDOW_BG = '#f0f0f0'
TEXT_DISABLED_BG = '#f5f5f5'

# Text colors
TEXT_PRIMARY_FG = '#000000'
TEXT_SECONDARY_FG = 'gray'

# ============================================================================
# FONTS
# ============================================================================

# Main title and section headers
FONT_TITLE = ('Arial', 16, 'bold')
FONT_SUBTITLE = ('Arial', 10)

# Label fonts
FONT_LABEL_BOLD = ('Arial', 10, 'bold')
FONT_LABEL = ('Arial', 9)

# Monospace fonts (for data display and code)
FONT_MONOSPACE = ('Courier', 9)

# ============================================================================
# DIMENSIONS
# ============================================================================

# Window dimensions (can be overridden by config.json)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# Text widget dimensions
TEXT_HEIGHT_SMALL = 3
TEXT_HEIGHT_LARGE = 25
TEXT_WIDTH_NORMAL = 60
TEXT_WIDTH_WIDE = 80

# Entry widget dimensions
ENTRY_WIDTH = 40

# ============================================================================
# PADDING AND SPACING
# ============================================================================

# Frame padding (internal spacing)
FRAME_PADDING = 15
NOTEBOOK_PADDING = 10
TITLE_FRAME_PADDING_X = 20
TITLE_FRAME_PADDING_Y = 10

# Grid padding (between elements)
GRID_PADDING_TOP = 0
GRID_PADDING_BOTTOM_SMALL = 5
GRID_PADDING_BOTTOM_MEDIUM = 10
GRID_PADDING_BOTTOM_LARGE = 15
GRID_PADDING_BOTTOM_XLARGE = 20

# Padding tuples for common combinations
PADY_LABEL = (GRID_PADDING_TOP, GRID_PADDING_BOTTOM_SMALL)
PADY_WIDGET = (GRID_PADDING_TOP, GRID_PADDING_BOTTOM_MEDIUM)
PADY_BUTTON = (GRID_PADDING_TOP, GRID_PADDING_BOTTOM_LARGE)
PADY_SECTION = (GRID_PADDING_TOP, GRID_PADDING_BOTTOM_XLARGE)

# Pack padding
PACK_PADDING_SMALL = (0, 5)
PACK_PADDING_MEDIUM = (0, 10)
PACK_PADDING_LARGE = (0, 20)

# Notebook and outer padding
NOTEBOOK_PADX = 10
NOTEBOOK_PADY = 10

# ============================================================================
# TAB NAMES
# ============================================================================

TAB_PROTECT = "Protect Data"
TAB_REVEAL = "Reveal Data"
TAB_PERFORMANCE = "Performance & Liveness"
TAB_STATUS = "Status & Info"

# ============================================================================
# BUTTON LABELS
# ============================================================================

BUTTON_PROTECT_DATA = "Protect Data"
BUTTON_COPY_PROTECTED = "Copy Protected Data"
BUTTON_REVEAL_DATA = "Reveal Data"
BUTTON_COPY_REVEALED = "Copy Revealed Data"
BUTTON_FETCH_METRICS = "Fetch Metrics"
BUTTON_CHECK_LIVENESS = "Check Liveness"
BUTTON_REFRESH_STATUS = "Refresh Status"

# ============================================================================
# LABEL TEXTS
# ============================================================================

LABEL_DATA_TO_PROTECT = "Data to Protect:"
LABEL_PROTECTION_POLICY = "Protection Policy:"
LABEL_PROTECTED_DATA = "Protected Data (Cipher):"
LABEL_REVEALED_DATA = "Revealed Data:"
LABEL_USERNAME = "Username:"
LABEL_USERNAME_HELP = "CipherTrust will determine how data is revealed based on this username"
LABEL_PERFORMANCE_METRICS = "Performance Metrics:"
LABEL_LIVENESS_STATUS = "Liveness Status:"
LABEL_CONNECTION_STATUS = "Connection Status:"

# ============================================================================
# COMMON TEXT STYLES
# ============================================================================

# Application title
APP_TITLE = "CRDP Data Protection"
APP_SUBTITLE = "Secure data encryption and tokenization"

# ============================================================================
# GRID LAYOUT STYLES
# ============================================================================

# Common grid sticky values
STICKY_W = 'w'
STICKY_EW = 'ew'
STICKY_NSEW = 'nsew'

# ============================================================================
# SEPARATOR STYLES
# ============================================================================

SEPARATOR_ORIENTATION = 'horizontal'
SEPARATOR_PADDING_Y = 10

# ============================================================================
# STATUS BAR STYLES
# ============================================================================

# Status bar colors
STATUS_BAR_BG = '#e0e0e0'
STATUS_BAR_FG = '#000000'
STATUS_BAR_SUCCESS_FG = '#008000'
STATUS_BAR_ERROR_FG = '#ff0000'

# Status bar fonts
STATUS_BAR_FONT = ('Arial', 9)

# Status bar height and padding
STATUS_BAR_HEIGHT = 1
STATUS_BAR_PADX = 10
STATUS_BAR_PADY = 5
