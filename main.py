from flask import Flask, request, jsonify, render_template, send_file, redirect
import os, random, string, json
uploads = json.load(open("uploads.json", 'r'))
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads"
exts = [".gif", ".png", ".jpeg", ".jpg", ".webm", ".mkv", ".avi", ".wmv", ".mov", ".mp4"]
emojis = ['😀', '😁', '😂', '🤣', '😃', '😄', '😅', '😆', '😉', '😊', '😋', '😎', '😍', '😘', '🥰', '😗', '😙', '😚', '☺️', '🙂', '🤗', '🤩', '🤔', '🤨', '😐', '😑', '😶', '🙄', '😏', '😣', '😥', '😮', '🤐', '😯', '😪', '😫', '😴', '😌', '😛', '😜', '😝', '🤤', '😒', '😓', '😔', '😕', '🙃', '🤑', '😲', '☹️', '🙁', '😖', '😞', '😟', '😤', '😢', '😭', '😦', '😧', '😨', '😩', '🤯', '😬', '😰', '😱', '🥵', '🥶', '😳', '🤪', '😵', '😡', '😠', '🤬', '😷', '🤒', '🤕', '🤢', '🤮', '🤧', '😇', '🤠', '🥳', '🥴', '🥺', '🤥', '🤫', '🤭', '🧐', '🤓', '😈', '👿', '🤡', '👹', '👺', '💀', '☠️', '👻', '👽', '👾', '🤖', '💩', '😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾', '🙈', '🙉', '🙊', '👶', '👶🏻', '👶🏼', '👶🏽', '👶🏾', '👶🏿', '🧒', '🧒🏻', '🧒🏼', '🧒🏽', '🧒🏾', '🧒🏿', '👦', '👦🏻', '👦🏼', '👦🏽', '👦🏾', '👦🏿', '👧', '👧🏻', '👧🏼', '👧🏽', '👧🏾', '👧🏿', '🧑', '🧑🏻', '🧑🏼', '🧑🏽', '🧑🏾', '🧑🏿', '👨', '👨🏻', '👨🏼', '👨🏽', '👨🏾', '👨🏿', '👩', '👩🏻', '👩🏼', '👩🏽', '👩🏾', '👩🏿', '🧓', '🧓🏻', '🧓🏼', '🧓🏽', '🧓🏾', '🧓🏿', '👴', '👴🏻', '👴🏼', '👴🏽', '👴🏾', '👴🏿', '👵', '👵🏻', '👵🏼', '👵🏽', '👵🏾', '👵🏿', '🤵', '🤵🏻', '🤵🏼', '🤵🏽', '🤵🏾', '🤵🏿', '👰', '👰🏻', '👰🏼', '👰🏽', '👰🏾', '👰🏿', '🤰', '🤰🏻', '🤰🏼', '🤰🏽', '🤰🏾', '🤰🏿', '🤱', '🤱🏻', '🤱🏼', '🤱🏽', '🤱🏾', '🤱🏿', '👼', '👼🏻', '👼🏼', '👼🏽', '👼🏾', '👼🏿', '🎅', '🎅🏻', '🎅🏼', '🎅🏽', '🎅🏾', '🎅🏿', '🤶', '🤶🏻', '🤶🏼', '🤶🏽', '🤶🏾', '🤶🏿', '🦸', '🦸🏻', '🦸🏼', '🦸🏽', '🦸🏾', '🦸🏿', '🤳', '🤳🏻', '🤳🏼', '🤳🏽', '🤳🏾', '🤳🏿', '💪', '💪🏻', '💪🏼', '💪🏽', '💪🏾', '💪🏿', '🦵', '🦵🏻', '🦵🏼', '🦵🏽', '🦵🏾', '🦵🏿', '🦶', '🦶🏻', '🦶🏼', '🦶🏽', '🦶🏾', '🦶🏿', '👈', '👈🏻', '👈🏼', '👈🏽', '👈🏾', '👈🏿', '👉', '👉🏻', '👉🏼', '👉🏽', '👉🏾', '👉🏿', '☝️', '☝🏻', '☝🏼', '☝🏽', '☝🏾', '☝🏿', '👆', '👆🏻', '👆🏼', '👆🏽', '👆🏾', '👆🏿', '🖕', '🖕🏻', '🖕🏼', '🖕🏽', '🖕🏾', '🖕🏿', '👇', '👇🏻', '👇🏼', '👇🏽', '👇🏾', '👇🏿', '✌️', '✌🏻', '✌🏼', '✌🏽', '✌🏾', '✌🏿', '🤞', '🤞🏻', '🤞🏼', '🤞🏽', '🤞🏾', '🤞🏿', '🖖', '🖖🏻', '🖖🏼', '🖖🏽', '🖖🏾', '🖖🏿', '🤘', '🤘🏻', '🤘🏼', '🤘🏽', '🤘🏾', '🤘🏿', '🤙', '🤙🏻', '🤙🏼', '🤙🏽', '🤙🏾', '🤙🏿', '🖐️', '🖐🏻', '🖐🏼', '🖐🏽', '🖐🏾', '🖐🏿', '✋', '✋🏻', '✋🏼', '✋🏽', '✋🏾', '✋🏿', '👌', '👌🏻', '👌🏼', '👌🏽', '👌🏾', '👌🏿', '👍', '👍🏻', '👍🏼', '👍🏽', '👍🏾', '👍🏿', '👎', '👎🏻', '👎🏼', '👎🏽', '👎🏾', '👎🏿', '✊', '✊🏻', '✊🏼', '✊🏽', '✊🏾', '✊🏿', '👊', '👊🏻', '👊🏼', '👊🏽', '👊🏾', '👊🏿', '🤛', '🤛🏻', '🤛🏼', '🤛🏽', '🤛🏾', '🤛🏿', '🤜', '🤜🏻', '🤜🏼', '🤜🏽', '🤜🏾', '🤜🏿', '🤚', '🤚🏻', '🤚🏼', '🤚🏽', '🤚🏾', '🤚🏿', '👋', '👋🏻', '👋🏼', '👋🏽', '👋🏾', '👋🏿', '🤟', '🤟🏻', '🤟🏼', '🤟🏽', '🤟🏾', '🤟🏿', '✍️', '✍🏻', '✍🏼', '✍🏽', '✍🏾', '✍🏿', '👏', '👏🏻', '👏🏼', '👏🏽', '👏🏾', '👏🏿', '👐', '👐🏻', '👐🏼', '👐🏽', '👐🏾', '👐🏿', '🙌', '🙌🏻', '🙌🏼', '🙌🏽', '🙌🏾', '🙌🏿', '🤲', '🤲🏻', '🤲🏼', '🤲🏽', '🤲🏾', '🤲🏿', '🙏', '🙏🏻', '🙏🏼', '🙏🏽', '🙏🏾', '🙏🏿', '🤝', '💅', '💅🏻', '💅🏼', '💅🏽', '💅🏾', '💅🏿', '👂', '👂🏻', '👂🏼', '👂🏽', '👂🏾', '👂🏿', '👃', '👃🏻', '👃🏼', '👃🏽', '👃🏾', '👃🏿', '🦰', '🦱', '🦲', '🦳', '👣', '👀', '👁️', '🧠', '🦴', '🦷', '👅', '👄', '💋', '💘', '❤️', '💓', '💔', '💕', '💖', '💗', '💙', '💚', '💛', '🧡', '💜', '🖤', '💝', '💞', '💟', '❣️', '💌', '💤', '💢', '💣', '💥', '💦', '💨', '💫', '💬', '🗨️', '🗯️', '💭', '🕳️', '👓', '🕶️', '🥽', '🥼', '👔', '👕', '👖', '🧣', '🧤', '🧥', '🧦', '👗', '👘', '👙', '👚', '👛', '👜', '👝', '🛍️', '🎒', '👞', '👟', '🥾', '🥿', '👠', '👡', '👢', '👑', '👒', '🎩', '🎓', '🧢', '⛑️', '📿', '💄', '💍', '💎', '🐵', '🐒', '🦍', '🐶', '🐕', '🐩', '🐺', '🦊', '🦝', '🐱', '🐈', '🦁', '🐯', '🐅', '🐆', '🐴', '🐎', '🦄', '🦓', '🦌', '🐮', '🐂', '🐃', '🐄', '🐷', '🐖', '🐗', '🐽', '🐏', '🐑', '🐐', '🐪', '🐫', '🦙', '🦒', '🐘', '🦏', '🦛', '🐭', '🐁', '🐀', '🐹', '🐰', '🐇', '🐿️', '🦔', '🦇', '🐻', '🐨', '🐼', '🦘', '🦡', '🐾', '🦃', '🐔', '🐓', '🐣', '🐤', '🐥', '🐦', '🐧', '🕊️', '🦅', '🦆', '🦢', '🦉', '🦚', '🦜', '🐸', '🐊', '🐢', '🦎', '🐍', '🐲', '🐉', '🦕', '🦖', '🐳', '🐋', '🐬', '🐟', '🐠', '🐡', '🦈', '🐙', '🐚', '🦀', '🦞', '🦐', '🦑', '🐌', '🦋', '🐛', '🐜', '🐝', '🐞', '🦗', '🕷️', '🕸️', '🦂', '🦟', '🦠', '💐', '🌸', '💮', '🏵️', '🌹', '🥀', '🌺', '🌻', '🌼', '🌷', '🌱', '🌲', '🌳', '🌴', '🌵', '🌾', '🌿', '☘️', '🍀', '🍁', '🍂', '🍃', '🍇', '🍈', '🍉', '🍊', '🍋', '🍌', '🍍', '🥭', '🍎', '🍏', '🍐', '🍑', '🍒', '🍓', '🥝', '🍅', '🥥', '🥑', '🍆', '🥔', '🥕', '🌽', '🌶️', '🥒', '🥬', '🥦', '🍄', '🥜', '🌰', '🍞', '🥐', '🥖', '🥨', '🥯', '🥞', '🧀', '🍖', '🍗', '🥩', '🥓', '🍔', '🍟', '🍕', '🌭', '🥪', '🌮', '🌯', '🥙', '🥚', '🍳', '🥘', '🍲', '🥣', '🥗', '🍿', '🧂', '🥫', '🍱', '🍘', '🍙', '🍚', '🍛', '🍜', '🍝', '🍠', '🍢', '🍣', '🍤', '🍥', '🥮', '🍡', '🥟', '🥠', '🥡', '🍦', '🍧', '🍨', '🍩', '🍪', '🎂', '🍰', '🧁', '🥧', '🍫', '🍬', '🍭', '🍮', '🍯', '🍼', '🥛', '☕', '🍵', '🍶', '🍾', '🍷', '🍸', '🍹', '🍺', '🍻', '🥂', '🥃', '🥤', '🥢', '🍽️', '🍴', '🥄', '🔪', '🏺', '🌍', '🌎', '🌏', '🌐', '🗺️', '🗾', '🧭', '🏔️', '⛰️', '🌋', '🗻', '🏕️', '🏖️', '🏜️', '🏝️', '🏞️', '🏟️', '🏛️', '🏗️', '🧱', '🏘️', '🏚️', '🏠', '🏡', '🏢', '🏣', '🏤', '🏥', '🏦', '🏨', '🏩', '🏪', '🏫', '🏬', '🏭', '🏯', '🏰', '💒', '🗼', '🗽', '⛪', '🕌', '🕍', '⛩️', '🕋', '⛲', '⛺', '🌁', '🌃', '🏙️', '🌄', '🌅', '🌆', '🌇', '🌉', '♨️', '🌌', '🎠', '🎡', '🎢', '💈', '🎪', '🚂', '🚃', '🚄', '🚅', '🚆', '🚇', '🚈', '🚉', '🚊', '🚝', '🚞', '🚋', '🚌', '🚍', '🚎', '🚐', '🚑', '🚒', '🚓', '🚔', '🚕', '🚖', '🚗', '🚘', '🚙', '🚚', '🚛', '🚜', '🚲', '🛴', '🛹', '🛵', '🚏', '🛣️', '🛤️', '🛢️', '⛽', '🚨', '🚥', '🚦', '🛑', '🚧', '⚓', '⛵', '🛶', '🚤', '🛳️', '⛴️', '🛥️', '🚢', '✈️', '🛩️', '🛫', '🛬', '💺', '🚁', '🚟', '🚠', '🚡', '🛰️', '🚀', '🛸', '🛎️', '🧳', '⌛', '⏳', '⌚', '⏰', '⏱️', '⏲️', '🕰️', '🕛', '🕧', '🕐', '🕜', '🕑', '🕝', '🕒', '🕞', '🕓', '🕟', '🕔', '🕠', '🕕', '🕡', '🕖', '🕢', '🕗', '🕣', '🕘', '🕤', '🕙', '🕥', '🕚', '🕦', '🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘', '🌙', '🌚', '🌛', '🌜', '🌡️', '☀️', '🌝', '🌞', '⭐', '🌟', '🌠', '☁️', '⛅', '⛈️', '🌤️', '🌥️', '🌦️', '🌧️', '🌨️', '🌩️', '🌪️', '🌫️', '🌬️', '🌀', '🌈', '🌂', '☂️', '☔', '⛱️', '⚡', '❄️', '☃️', '⛄', '☄️', '🔥', '💧', '🌊', '🎃', '🎄', '🎆', '🎇', '🧨', '✨', '🎈', '🎉', '🎊', '🎋', '🎍', '🎎', '🎏', '🎐', '🎑', '🧧', '🎀', '🎁', '🎗️', '🎟️', '🎫', '🎖️', '🏆', '🏅', '🥇', '🥈', '🥉', '⚽', '⚾', '🥎', '🏀', '🏐', '🏈', '🏉', '🎾', '🥏', '🎳', '🏏', '🏑', '🏒', '🥍', '🏓', '🏸', '🥊', '🥋', '🥅', '⛳', '⛸️', '🎣', '🎽', '🎿', '🛷', '🥌', '🎯', '🎱', '🔮', '🧿', '🎮', '🕹️', '🎰', '🎲', '🧩', '🧸', '♠️', '♥️', '♦️', '♣️', '♟️', '🃏', '🀄', '🎴', '🎭', '🖼️', '🎨', '🧵', '🧶', '🔇', '🔈', '🔉', '🔊', '📢', '📣', '📯', '🔔', '🔕', '🎼', '🎵', '🎶', '🎙️', '🎚️', '🎛️', '🎤', '🎧', '📻', '🎷', '🎸', '🎹', '🎺', '🎻', '🥁', '📱', '📲', '☎️', '📞', '📟', '📠', '🔋', '🔌', '💻', '🖥️', '🖨️', '⌨️', '🖱️', '🖲️', '💽', '💾', '💿', '📀', '🧮', '🎥', '🎞️', '📽️', '🎬', '📺', '📷', '📸', '📹', '📼', '🔍', '🔎', '🕯️', '💡', '🔦', '🏮', '📔', '📕', '📖', '📗', '📘', '📙', '📚', '📓', '📒', '📃', '📜', '📄', '📰', '🗞️', '📑', '🔖', '🏷️', '💰', '💴', '💵', '💶', '💷', '💸', '💳', '🧾', '💹', '💱', '💲', '✉️', '📧', '📨', '📩', '📤', '📥', '📦', '📫', '📪', '📬', '📭', '📮', '🗳️', '✏️', '✒️', '🖋️', '🖊️', '🖌️', '🖍️', '📝', '💼', '📁', '📂', '🗂️', '📅', '📆', '🗒️', '🗓️', '📇', '📈', '📉', '📊', '📋', '📌', '📍', '📎', '🖇️', '📏', '📐', '✂️', '🗃️', '🗄️', '🗑️', '🔒', '🔓', '🔏', '🔐', '🔑', '🗝️', '🔨', '⛏️', '⚒️', '🛠️', '🗡️', '⚔️', '🔫', '🏹', '🛡️', '🔧', '🔩', '⚙️', '🗜️', '⚖️', '🔗', '⛓️', '🧰', '🧲', '⚗️', '🧪', '🧫', '🧬', '🔬', '🔭', '📡', '💉', '💊', '🚪', '🛏️', '🛋️', '🚽', '🚿', '🛁', '🧴', '🧷', '🧹', '🧺', '🧻', '🧼', '🧽', '🧯', '🛒', '🚬', '⚰️', '⚱️', '🗿', '🏧', '🚮', '🚰', '♿', '🚹', '🚺', '🚻', '🚼', '🚾', '🛂', '🛃', '🛄', '🛅', '⚠️', '🚸', '⛔', '🚫', '🚳', '🚭', '🚯', '🚱', '🚷', '📵', '🔞', '☢️', '☣️', '⬆️', '↗️', '➡️', '↘️', '⬇️', '↙️', '⬅️', '↖️', '↕️', '↔️', '↩️', '↪️', '⤴️', '⤵️', '🔃', '🔄', '🔙', '🔚', '🔛', '🔜', '🔝', '🛐', '⚛️', '🕉️', '✡️', '☸️', '☯️', '✝️', '☦️', '☪️', '☮️', '🕎', '🔯', '♈', '♉', '♊', '♋', '♌', '♍', '♎', '♏', '♐', '♑', '♒', '♓', '⛎', '🔀', '🔁', '🔂', '▶️', '⏩', '⏭️', '⏯️', '◀️', '⏪', '⏮️', '🔼', '⏫', '🔽', '⏬', '⏸️', '⏹️', '⏺️', '⏏️', '🎦', '🔅', '🔆', '📶', '📳', '📴', '♀️', '♂️', '⚕️', '♾️', '♻️', '⚜️', '🔱', '📛', '🔰', '⭕', '✅', '☑️', '✔️', '✖️', '❌', '❎', '➕', '➖', '➗', '➰', '➿', '〽️', '✳️', '✴️', '❇️', '‼️', '⁉️', '❓', '❔', '❕', '❗', '〰️', '©️', '®️', '🔟', '💯', '🔠', '🔡', '🔢', '🔣', '🔤', '🅰️', '🆎', '🅱️', '🆑', '🆒', '🆓', 'ℹ️', '🆔', 'Ⓜ️', '🆕', '🆖', '🅾️', '🆗', '🅿️', '🆘', '🆙', '🆚', '🈁', '🈂️', '🈷️', '🈶', '🈯', '🉐', '🈹', '🈚', '🈲', '🉑', '🈸', '🈴', '🈳', '㊗️', '㊙️', '🈺', '🈵', '▪️', '▫️', '◻️', '◼️', '◽', '◾', '⬛', '⬜', '🔶', '🔷', '🔸', '🔹', '🔺', '🔻', '💠', '🔘', '🔲', '🔳', '⚪', '⚫', '🔴', '🔵', '🏁', '🚩', '🎌', '🏴', '🏳️', '🇦🇨', '🇦🇩', '🇦🇪', '🇦🇫', '🇦🇬', '🇦🇮', '🇦🇱', '🇦🇲', '🇦🇴', '🇦🇶', '🇦🇷', '🇦🇸', '🇦🇹', '🇦🇺', '🇦🇼', '🇦🇽', '🇦🇿', '🇧🇦', '🇧🇧', '🇧🇩', '🇧🇪', '🇧🇫', '🇧🇬', '🇧🇭', '🇧🇮', '🇧🇯', '🇧🇱', '🇧🇲', '🇧🇳', '🇧🇴', '🇧🇶', '🇧🇷', '🇧🇸', '🇧🇹', '🇧🇻', '🇧🇼', '🇧🇾', '🇧🇿', '🇨🇦', '🇨🇨', '🇨🇩', '🇨🇫', '🇨🇬', '🇨🇭', '🇨🇮', '🇨🇰', '🇨🇱', '🇨🇲', '🇨🇳', '🇨🇴', '🇨🇵', '🇨🇷', '🇨🇺', '🇨🇻', '🇨🇼', '🇨🇽', '🇨🇾', '🇨🇿', '🇩🇪', '🇩🇬', '🇩🇯', '🇩🇰', '🇩🇲', '🇩🇴', '🇩🇿', '🇪🇦', '🇪🇨', '🇪🇪', '🇪🇬', '🇪🇭', '🇪🇷', '🇪🇸', '🇪🇹', '🇪🇺', '🇫🇮', '🇫🇯', '🇫🇰', '🇫🇲', '🇫🇴', '🇫🇷', '🇬🇦', '🇬🇧', '🇬🇩', '🇬🇪', '🇬🇫', '🇬🇬', '🇬🇭', '🇬🇮', '🇬🇱', '🇬🇲', '🇬🇳', '🇬🇵', '🇬🇶', '🇬🇷', '🇬🇸', '🇬🇹', '🇬🇺', '🇬🇼', '🇬🇾', '🇭🇰', '🇭🇲', '🇭🇳', '🇭🇷', '🇭🇹', '🇭🇺', '🇮🇨', '🇮🇩', '🇮🇪', '🇮🇱', '🇮🇲', '🇮🇳', '🇮🇴', '🇮🇶', '🇮🇷', '🇮🇸', '🇮🇹', '🇯🇪', '🇯🇲', '🇯🇴', '🇯🇵', '🇰🇪', '🇰🇬', '🇰🇭', '🇰🇮', '🇰🇲', '🇰🇳', '🇰🇵', '🇰🇷', '🇰🇼', '🇰🇾', '🇰🇿', '🇱🇦', '🇱🇧', '🇱🇨', '🇱🇮', '🇱🇰', '🇱🇷', '🇱🇸', '🇱🇹', '🇱🇺', '🇱🇻', '🇱🇾', '🇲🇦', '🇲🇨', '🇲🇩', '🇲🇪', '🇲🇫', '🇲🇬', '🇲🇭', '🇲🇰', '🇲🇱', '🇲🇲', '🇲🇳', '🇲🇴', '🇲🇵', '🇲🇶', '🇲🇷', '🇲🇸', '🇲🇹', '🇲🇺', '🇲🇻', '🇲🇼', '🇲🇽', '🇲🇾', '🇲🇿', '🇳🇦', '🇳🇨', '🇳🇪', '🇳🇫', '🇳🇬', '🇳🇮', '🇳🇱', '🇳🇴', '🇳🇵', '🇳🇷', '🇳🇺', '🇳🇿', '🇴🇲', '🇵🇦', '🇵🇪', '🇵🇫', '🇵🇬', '🇵🇭', '🇵🇰', '🇵🇱', '🇵🇲', '🇵🇳', '🇵🇷', '🇵🇸', '🇵🇹', '🇵🇼', '🇵🇾', '🇶🇦', '🇷🇪', '🇷🇴', '🇷🇸', '🇷🇺', '🇷🇼', '🇸🇦', '🇸🇧', '🇸🇨', '🇸🇩', '🇸🇪', '🇸🇬', '🇸🇭', '🇸🇮', '🇸🇯', '🇸🇰', '🇸🇱', '🇸🇲', '🇸🇳', '🇸🇴', '🇸🇷', '🇸🇸', '🇸🇹', '🇸🇻', '🇸🇽', '🇸🇾', '🇸🇿', '🇹🇦', '🇹🇨', '🇹🇩', '🇹🇫', '🇹🇬', '🇹🇭', '🇹🇯', '🇹🇰', '🇹🇱', '🇹🇲', '🇹🇳', '🇹🇴', '🇹🇷', '🇹🇹', '🇹🇻', '🇹🇼', '🇹🇿', '🇺🇦', '🇺🇬', '🇺🇲', '🇺🇳', '🇺🇸', '🇺🇾', '🇺🇿', '🇻🇦', '🇻🇨', '🇻🇪', '🇻🇬', '🇻🇮', '🇻🇳', '🇻🇺', '🇼🇫', '🇼🇸', '🇽🇰', '🇾🇪', '🇾🇹', '🇿🇦', '🇿🇲', '🇿🇼']
dictlol = {
    ".gif":  ["og:image", "og:image:secure_url", "og:image:url", "summary_large_image"],
    ".png":  ["og:image", "og:image:secure_url", "og:image:url", "summary_large_image"],
    ".jpeg": ["og:image", "og:image:secure_url", "og:image:url", "summary_large_image"],
    ".jpg":  ["og:image", "og:image:secure_url", "og:image:url", "summary_large_image"],
    ".webm": ["og:video", "twitter:player", "twitter:player:stream", "player"],
    ".mkv":  ["og:video", "twitter:player", "twitter:player:stream", "player"],
    ".avi":  ["og:video", "twitter:player", "twitter:player:stream", "player"],
    ".wmv":  ["og:video", "twitter:player", "twitter:player:stream", "player"],
    ".mov":  ["og:video", "twitter:player", "twitter:player:stream", "player"],
    ".mp4":  ["og:video", "twitter:player", "twitter:player:stream", "player"]
}
@app.errorhandler(400)
def error_400(error):
    return '<style>body{background-color: rgb(30, 30, 30);}.text{text-align: center; font-family: monospace; position: relative; top: 15%; color: rgb(255, 255, 255); text-shadow: 0px 0px 4px #ffffff;}</style><div class="text"> <h1>>.&#60;</h1> <h3>400</h3></div>', 400

@app.errorhandler(401)
def error_401(error):
    return '<style>body{background-color: rgb(30, 30, 30);}.text{text-align: center; font-family: monospace; position: relative; top: 15%; color: rgb(255, 255, 255); text-shadow: 0px 0px 4px #ffffff;}</style><div class="text"> <h1>>.&#60;</h1> <h3>401</h3></div>', 401

@app.errorhandler(403)
def error_403(error):
    return '<style>body{background-color: rgb(30, 30, 30);}.text{text-align: center; font-family: monospace; position: relative; top: 15%; color: rgb(255, 255, 255); text-shadow: 0px 0px 4px #ffffff;}</style><div class="text"> <h1>>.&#60;</h1> <h3>403</h3></div>', 403

@app.errorhandler(404)
def error_404(error):
    return '<style>body{background-color: rgb(30, 30, 30);}.text{text-align: center; font-family: monospace; position: relative; top: 15%; color: rgb(255, 255, 255); text-shadow: 0px 0px 4px #ffffff;}</style><div class="text"> <h1>>.&#60;</h1> <h3>404</h3></div>', 404

@app.errorhandler(405)
def error_405(error):
    return '<style>body{background-color: rgb(30, 30, 30);}.text{text-align: center; font-family: monospace; position: relative; top: 15%; color: rgb(255, 255, 255); text-shadow: 0px 0px 4px #ffffff;}</style><div class="text"> <h1>>.&#60;</h1> <h3>405</h3></div>', 405

@app.errorhandler(429)
def error_429(error):
    return '<style>body{background-color: rgb(30, 30, 30);}.text{text-align: center; font-family: monospace; position: relative; top: 15%; color: rgb(255, 255, 255); text-shadow: 0px 0px 4px #ffffff;}</style><div class="text"> <h1>>.&#60;</h1> <h3>429</h3></div>', 429

@app.errorhandler(500)
def error_500(error):
    return '<style>body{background-color: rgb(30, 30, 30);}.text{text-align: center; font-family: monospace; position: relative; top: 15%; color: rgb(255, 255, 255); text-shadow: 0px 0px 4px #ffffff;}</style><div class="text"> <h1>>.&#60;</h1> <h3>500</h3></div>', 500

@app.errorhandler(502)
def error_502(error):
    return '<style>body{background-color: rgb(30, 30, 30);}.text{text-align: center; font-family: monospace; position: relative; top: 15%; color: rgb(255, 255, 255); text-shadow: 0px 0px 4px #ffffff;}</style><div class="text"> <h1>>.&#60;</h1> <h3>502</h3></div>', 502

@app.errorhandler(503)
def error_503(error):
    return '<style>body{background-color: rgb(30, 30, 30);}.text{text-align: center; font-family: monospace; position: relative; top: 15%; color: rgb(255, 255, 255); text-shadow: 0px 0px 4px #ffffff;}</style><div class="text"> <h1>>.&#60;</h1> <h3>503</h3></div>', 503

@app.errorhandler(504)
def error_504(error):
    return '<style>body{background-color: rgb(30, 30, 30);}.text{text-align: center; font-family: monospace; position: relative; top: 15%; color: rgb(255, 255, 255); text-shadow: 0px 0px 4px #ffffff;}</style><div class="text"> <h1>>.&#60;</h1> <h3>504</h3></div>', 504

@app.route("/")
def index():
    return redirect("https://neutralising.github.io/images/")

@app.route("/cfg")
def cfg():
    return send_file("uploader.sxcu", as_attachment=True)

@app.route("/<f>")
def files(f):
    uplds = json.load(open("uploads.json", 'r'))
    if f == "favicon.ico":
        return "Annoying asf"
    elif f not in uplds:
        return '<style>body{background-color: rgb(30, 30, 30);}.text{text-align: center; font-family: monospace; position: relative; top: 15%; color: rgb(255, 255, 255); text-shadow: 0px 0px 4px #ffffff;}</style><div class="text"> <h1>>.&#60;</h1> <h3>404</h3></div>', 404
    else:
        return render_template(uplds.get(f) + ".html")

@app.route("/i/<f>")
def send_f(f):
    if os.path.exists(f"uploads/{f}") == False:
        return '<style>body{background-color: rgb(30, 30, 30);}.text{text-align: center; font-family: monospace; position: relative; top: 15%; color: rgb(255, 255, 255); text-shadow: 0px 0px 4px #ffffff;}</style><div class="text"> <h1>>.&#60;</h1> <h3>404</h3></div>', 404
    else:
        return send_file(f"uploads/{f}")

@app.route("/domains")
def domains():
    return redirect("https://raw.githubusercontent.com/neutralising/images/main/domains")

@app.route("/api/upload", methods=["POST"])
def upload():
    ok = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    if os.path.exists(f"templates/{ok}.html") == True:
        ok = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    chars = "0123456789abcdef"
    color = ''.join(random.choices(chars, k=6))
    file = request.files["file"]
    filename = file.filename
    filename = filename.lower()
    fileext = os.path.splitext(filename)[-1].lower()
    if fileext in exts:
        if request.headers.get("title") == None:
            title = "astolfo is hot"
        else:
            title = request.headers.get("title")
        if request.headers.get("description") == None:
            description = "Anything > sxcu.net"
        else:
            description = request.headers.get("description")
        if request.headers.get("urltype") == "invis":
            imgpath = "".join(random.choices(["​"], k=random.randint(8, 64)))
        elif request.headers.get("urltype") == "emoji":
            imgpath  = "".join(random.choices(emojis, k=random.randint(8, 32)))
        else:
            imgpath = ok
        if request.headers.get("fakeurl") == None:
            url = "https://" + request.headers["host"] + "/" + imgpath
        else:
            url = "<" + request.headers.get("fakeurl") + ">" + "||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||" + "https://" + request.headers["host"] + "/" + imgpath
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], f"{ok}{fileext}"))
        html = open(f"templates/{ok}.html", "w")
        html.write(f'<meta property="og:title" content="{title}">\n<meta property="twitter:title" content="{title}">\n<meta property="og:description" content="{description}">\n<meta property="twitter:description" content="{description}">' + f'<meta property="og:url" content="https://{request.headers["host"]}/{ok}">\n' + f'<meta name="twitter:card" content="{dictlol.get(fileext)[3]}">\n' + f'<meta property="{dictlol.get(fileext)[0]}" content="https://{request.headers["host"]}/i/{ok}{fileext}">\n' + f'<meta property="{dictlol.get(fileext)[1]}" content="https://{request.headers["host"]}/i/{ok}{fileext}">\n' + f'<meta property="{dictlol.get(fileext)[2]}" content="https://{request.headers["host"]}/i/{ok}{fileext}">\n' + f'<meta name="theme-color" content="#{color}">\n' + f'<h1>bad at css</h1>\n<a href=https://{request.headers["host"]}/i/{ok}{fileext}>File here</a>')
        uploads[imgpath] = ok
        f = open("uploads.json", 'w')
        f.write(json.dumps(uploads, indent=4))
        f.close()
        return jsonify({"url": url})
    else:
        return jsonify({"error": "Invaild file extenstion (Vaild ones: .gif, .png, .jpeg, .jpg, .webm, .mkv, .avi, .wmv, .mov, .mp4)"}), 400

if __name__ == "__main__":
    ip = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 1337))
    app.run(host=ip, port=port,ssl_context=('cert.pem', 'key.pem'))
