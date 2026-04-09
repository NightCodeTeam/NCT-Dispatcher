export function not_to_long_text(bold_part, normal_part, max_length) {
    const full_text = `<b>${bold_part}</b>${normal_part}`;
    if (bold_part.length + normal_part.length > max_length) {
        const available_length = max_length - 3
        if (available_length <= 0) {
            return '...'
        }

        if (bold_part.length >= available_length) {
            return `<b>${bold_part.substring(0, available_length)}...</b>`
        } else {
            return `<b>${bold_part}</b> ${normal_part.substring(0, available_length - bold_part.length)}...`
        }
    }
    return full_text;
}