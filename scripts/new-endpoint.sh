#!/bin/bash
#
# Helper script to create new API endpoint documentation
# Usage: ./scripts/new-endpoint.sh
#

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DOC_DIR="$SCRIPT_DIR/../doc"
TEMPLATE_FILE="$DOC_DIR/docs/TEMPLATE.md"

echo "=========================================="
echo "FortiAnalyzer API - New Endpoint Creator"
echo "=========================================="
echo ""

# Display available categories
echo "Available categories:"
echo "  1) device-manager          - Device lifecycle operations"
echo "  2) logview                 - Log search operations"
echo "  3) fortiview*              - Analytics (IOC, Top Sources, etc.)"
echo "  4) reports                 - Report generation and management"
echo "  5) system-settings*        - System configuration"
echo "  6) incidents-events*       - Event handlers and alerts"
echo ""

# Get category
echo "Enter category (e.g., device-manager, logview):"
read -r category

if [ -z "$category" ]; then
    echo "Error: Category cannot be empty"
    exit 1
fi

# Get operation name
echo ""
echo "Enter operation name (use lowercase with hyphens):"
echo "Example: create-log-search-task, get-system-status"
read -r operation

if [ -z "$operation" ]; then
    echo "Error: Operation name cannot be empty"
    exit 1
fi

# Create category directory if it doesn't exist
CATEGORY_DIR="$DOC_DIR/docs/$category"
mkdir -p "$CATEGORY_DIR"

# Create the new file
NEW_FILE="$CATEGORY_DIR/$operation.md"

if [ -f "$NEW_FILE" ]; then
    echo ""
    echo "⚠️  Warning: File already exists: $NEW_FILE"
    echo "Do you want to overwrite? (y/N):"
    read -r overwrite
    if [[ ! "$overwrite" =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
fi

# Copy template
cp "$TEMPLATE_FILE" "$NEW_FILE"

# Get today's date
TODAY=$(date +"%B %d, %Y")

# Update the template with operation name
sed -i.bak "s/\[Operation Name\]/${operation}/g" "$NEW_FILE"
sed -i.bak "s/\[Date in format: November 10, 2025\]/${TODAY}/g" "$NEW_FILE"
rm "${NEW_FILE}.bak"

echo ""
echo "✅ Created: $NEW_FILE"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Next Steps:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Edit the file with your API details:"
echo "   $NEW_FILE"
echo ""
echo "2. Add to main index (doc/index.md):"
echo "   Add this line in the '$category' toctree section:"
echo "   docs/$category/$operation"
echo ""
echo "3. Test locally:"
echo "   cd doc/"
echo "   make livehtml"
echo ""
echo "4. Build and deploy:"
echo "   make clean"
echo "   make html"
echo "   make upload"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Offer to open in editor
echo "Open file in default editor? (y/N):"
read -r open_editor
if [[ "$open_editor" =~ ^[Yy]$ ]]; then
    if [ -n "$EDITOR" ]; then
        $EDITOR "$NEW_FILE"
    elif command -v code &> /dev/null; then
        code "$NEW_FILE"
    elif command -v vim &> /dev/null; then
        vim "$NEW_FILE"
    else
        open "$NEW_FILE"
    fi
fi
