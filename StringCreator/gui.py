"""NiceGUI desktop front-end for StringCreator.

A thin GUI layer over the existing StringCreator core. Run with:

    python gui.py

By default it opens a native desktop window (requires pywebview). Set the
environment variable STRINGCREATOR_GUI_NATIVE=0 to open in a browser tab instead.
"""
import os
from pathlib import Path

from nicegui import app, ui

import StringCreator as sc

ASSETS_DIR = Path(__file__).resolve().parent / 'assets'
app.add_static_files('/assets', str(ASSETS_DIR))

BRAND_OPTIONS = {'random': 'Random brand', **{b: b.capitalize() for b in sc.CREDIT_CARD_BRANDS}}
ENCODING_OPTIONS = {'none': 'None (plain text)', 'base64': 'Base64', 'url': 'URL',
                    'hex': 'Hex', 'html': 'HTML entities'}
VALIDATE_KINDS = {'personnummer': 'Swedish personnummer', 'luhn': 'Luhn checksum',
                  'creditcard': 'Credit card', 'password': 'Password strength'}
STRENGTH_TYPES = {1, 2, 9}

THEME_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&family=Orbitron:wght@600;800&display=swap" rel="stylesheet">
<style>
:root{
  --bg0:#0a0e14; --bg1:#0d1b2a; --neon:#00e676; --cyan:#00e5ff; --accent:#39ff14;
  --text:#e6f1ff; --muted:#7d8fa3; --panel:rgba(13,27,42,0.55); --border:rgba(0,230,118,0.28);
}
html, body, .q-page, .nicegui-content{ background:var(--bg0) !important; color:var(--text);
  font-family:'Inter',system-ui,sans-serif; }
.nicegui-content{ padding:0; }

/* animated background layers */
body::before{ content:''; position:fixed; inset:0; z-index:-2;
  background:
    radial-gradient(1200px 600px at 12% -10%, rgba(0,230,118,0.12), transparent 60%),
    radial-gradient(1000px 700px at 112% 8%, rgba(0,229,255,0.12), transparent 55%),
    linear-gradient(160deg, var(--bg1), var(--bg0) 70%);
  animation: pulseGlow 9s ease-in-out infinite; }
body::after{ content:''; position:fixed; inset:0; z-index:-1; pointer-events:none;
  background-image:
    linear-gradient(rgba(0,229,255,0.045) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,229,255,0.045) 1px, transparent 1px);
  background-size:42px 42px;
  -webkit-mask-image: radial-gradient(circle at 50% 22%, black, transparent 82%);
          mask-image: radial-gradient(circle at 50% 22%, black, transparent 82%); }
@keyframes pulseGlow{ 0%,100%{opacity:.85} 50%{opacity:1} }
.scanline{ position:fixed; left:0; right:0; height:140px; z-index:-1; pointer-events:none;
  background:linear-gradient(transparent, rgba(0,230,118,0.06), transparent);
  animation: scan 7.5s linear infinite; }
@keyframes scan{ 0%{transform:translateY(-140px)} 100%{transform:translateY(100vh)} }

/* glass panels */
.glass{ background:var(--panel) !important; border:1px solid var(--border) !important;
  border-radius:18px !important; -webkit-backdrop-filter:blur(10px); backdrop-filter:blur(10px);
  box-shadow: 0 0 0 1px rgba(0,229,255,0.05), 0 24px 60px rgba(0,0,0,0.45),
              inset 0 1px 0 rgba(255,255,255,0.04) !important; }

/* brand header */
.brand{ font-family:'Orbitron',sans-serif; font-weight:800; letter-spacing:1px; line-height:1.05;
  background:linear-gradient(90deg,var(--neon),var(--cyan)); -webkit-background-clip:text;
  background-clip:text; color:transparent; text-shadow:0 0 26px rgba(0,230,118,0.25); }
.tagline{ color:var(--muted); font-size:.72rem; letter-spacing:.22em; text-transform:uppercase; }
.divider-neon{ height:2px; border:none; margin:14px 0 6px;
  background:linear-gradient(90deg,transparent,var(--neon),var(--cyan),transparent); opacity:.6; }
.logo-glow{ filter:drop-shadow(0 0 10px rgba(0,230,118,0.45)); }
.section-title{ color:var(--cyan); font-family:'JetBrains Mono',monospace; font-size:.7rem;
  letter-spacing:.2em; text-transform:uppercase; opacity:.8; }

/* buttons */
.q-btn{ text-transform:none; font-weight:600; border-radius:12px; }
.neon-btn{ background:linear-gradient(90deg,var(--neon),var(--cyan)) !important; color:#04120a !important;
  box-shadow:0 0 18px rgba(0,230,118,0.35); }
.neon-btn:hover{ box-shadow:0 0 28px rgba(0,229,255,0.55); }
.ghost-btn{ color:var(--cyan) !important; border:1px solid var(--border) !important;
  background:rgba(0,229,255,0.04) !important; }
.ghost-btn:hover{ box-shadow:0 0 16px rgba(0,229,255,0.30); }

/* tabs */
.q-tab{ text-transform:none; font-weight:600; color:var(--muted); }
.q-tab--active{ color:var(--text); }
.q-tabs .q-tab__indicator{ height:3px; background:linear-gradient(90deg,var(--neon),var(--cyan));
  box-shadow:0 0 12px rgba(0,230,118,0.5); }

/* inputs */
.q-field--focused .q-field__control{ box-shadow:0 0 0 1px var(--cyan), 0 0 14px rgba(0,229,255,0.22); }

/* output */
.output textarea{ font-family:'JetBrains Mono',monospace !important; color:var(--neon) !important;
  letter-spacing:.02em; }

/* history table */
.q-table__container, .q-table{ background:transparent !important; color:var(--text) !important; }
.q-table thead th{ color:var(--cyan) !important; font-family:'JetBrains Mono',monospace;
  letter-spacing:.05em; }
.q-table tbody td{ font-family:'JetBrains Mono',monospace; color:var(--text) !important; }

/* scrollbar */
*::-webkit-scrollbar{ width:10px; height:10px; }
*::-webkit-scrollbar-track{ background:transparent; }
*::-webkit-scrollbar-thumb{ background:linear-gradient(var(--neon),var(--cyan)); border-radius:8px; }
</style>
"""

LOGO_HTML = '<img src="/assets/logo.svg" width="60" height="60" alt="StringCreator" class="logo-glow"/>'


def apply_theme():
    """Enable the neon dark theme (colors + fonts + custom CSS)."""
    ui.dark_mode().enable()
    ui.colors(primary='#00e676', secondary='#00e5ff', accent='#39ff14',
              dark='#0a0e14', dark_page='#0a0e14',
              positive='#00e676', negative='#ff4d6d', warning='#ffd166', info='#00e5ff')
    ui.add_head_html(THEME_CSS)


def _generate_values(type_num, length, use_all, brand, batch, unique, encoding):
    """Produce a list of generated strings using the shared core functions."""
    if use_all:
        return [sc.generate_string(0, type_num, True)]

    results, seen = [], set()
    attempts = 0
    max_attempts = max(batch * 50, 100)
    while len(results) < batch:
        if type_num == 19:
            value = sc.generate_credit_card(None if brand == 'random' else brand)
        else:
            value = sc.generate_string(length, type_num, False)

        if encoding and encoding != 'none':
            value = sc.encode_string(value, encoding)

        if unique and value in seen:
            attempts += 1
            if attempts > max_attempts:
                ui.notify(f'Only produced {len(results)} unique value(s) of {batch} requested',
                          type='warning')
                break
            continue

        seen.add(value)
        results.append(value)
    return results


def build_ui():
    apply_theme()
    ui.html('<div class="scanline"></div>')

    with ui.column().classes('w-full items-center px-4 pb-16'):
        with ui.column().classes('w-full max-w-3xl gap-4'):
            # hero header
            with ui.row().classes('items-center gap-4 mt-8'):
                ui.html(LOGO_HTML)
                with ui.column().classes('gap-0'):
                    ui.label('StringCreator').classes('brand text-4xl')
                    ui.label('Advanced string & security payload generator').classes('tagline mt-1')
            ui.html('<hr class="divider-neon"/>')

            with ui.tabs().classes('w-full') as tabs:
                generate_tab = ui.tab('Generate', icon='bolt')
                validate_tab = ui.tab('Validate', icon='verified')
                history_tab = ui.tab('History', icon='history')

            with ui.tab_panels(tabs, value=generate_tab).classes('w-full bg-transparent'):
                # ---- Generate ----
                with ui.tab_panel(generate_tab).classes('p-0'):
                    with ui.card().classes('glass w-full p-6 gap-4'):
                        ui.label('Configure').classes('section-title')
                        type_select = ui.select(
                            options={num: f'{num}. {label}' for num, label in sc.TYPE_LABELS.items()},
                            value=1, label='Type').classes('w-full')

                        with ui.row().classes('w-full items-center'):
                            length_input = ui.number('Length (bytes)', value=16, min=1, precision=0).classes('w-40')
                            batch_input = ui.number('Batch count', value=1, min=1, precision=0).classes('w-40')
                            unique_switch = ui.switch('Unique')

                        with ui.row().classes('w-full items-center'):
                            all_switch = ui.switch('All payloads')
                            brand_select = ui.select(options=BRAND_OPTIONS, value='random',
                                                     label='Card brand').classes('w-48')
                            encoding_select = ui.select(options=ENCODING_OPTIONS, value='none',
                                                        label='Encoding').classes('w-48')

                        output_area = ui.textarea(label='Output').props('readonly outlined').classes('w-full output')
                        info_label = ui.label('').classes('text-sm').style('color:var(--muted)')

                        def refresh_controls():
                            t = type_select.value
                            is_payload = t in sc.PAYLOAD_TYPES
                            is_fixed = t in sc.NO_LENGTH_TYPES
                            use_all = is_payload and all_switch.value
                            all_switch.set_visibility(is_payload)
                            brand_select.set_visibility(t == 19)
                            length_input.set_visibility(not is_fixed and not use_all)
                            batch_input.set_visibility(not use_all)
                            unique_switch.set_visibility(not use_all and (batch_input.value or 1) > 1)
                            encoding_select.set_visibility(not use_all)

                        def do_generate():
                            t = type_select.value
                            use_all = t in sc.PAYLOAD_TYPES and all_switch.value
                            length = int(length_input.value or 0)
                            batch = max(int(batch_input.value or 1), 1)
                            if not use_all and t not in sc.NO_LENGTH_TYPES and t not in sc.PAYLOAD_TYPES and length <= 0:
                                ui.notify('Length must be > 0 for this type', type='negative')
                                return

                            results = _generate_values(t, length, use_all, brand_select.value,
                                                       batch, unique_switch.value, encoding_select.value)
                            if not results:
                                return
                            final = '\n'.join(results) if len(results) != 1 else results[0]
                            output_area.value = final

                            parts = [f'{len(final.encode("utf-8"))} bytes']
                            if len(results) > 1:
                                parts.append(f'{len(results)} values')
                            if t in STRENGTH_TYPES and len(results) == 1:
                                strength, score, _ = sc.check_password_strength(final)
                                parts.append(f'Strength: {strength} ({score}/6)')
                            info_label.text = '  |  '.join(parts)

                            sc.save_to_history(final, t, length)

                        def do_copy():
                            if not output_area.value:
                                ui.notify('Nothing to copy', type='warning')
                                return
                            if sc.copy_to_clipboard(output_area.value):
                                ui.notify('Copied to clipboard', type='positive')
                            else:
                                ui.notify('Clipboard unavailable', type='negative')

                        type_select.on_value_change(refresh_controls)
                        all_switch.on_value_change(refresh_controls)
                        batch_input.on_value_change(refresh_controls)

                        with ui.row():
                            ui.button('Generate', on_click=do_generate).props('unelevated').classes('neon-btn')
                            ui.button('Copy', on_click=do_copy).props('flat').classes('ghost-btn')

                        # ---- Export ----
                        with ui.expansion('Export to file').classes('w-full'):
                            filename_input = ui.input('Filename', value='output.txt').classes('w-64')
                            format_select = ui.select({'text': 'Text', 'json': 'JSON', 'csv': 'CSV'},
                                                      value='text', label='Format').classes('w-40')

                            def do_save():
                                if not output_area.value:
                                    ui.notify('Generate something first', type='warning')
                                    return
                                results = output_area.value.split('\n')
                                try:
                                    sc.save_output(filename_input.value, results, format_select.value,
                                                   type_select.value, int(length_input.value or 0))
                                    ui.notify(f'Saved to {filename_input.value}', type='positive')
                                except OSError as e:
                                    ui.notify(f'Error saving: {e}', type='negative')

                            ui.button('Save', on_click=do_save).props('flat').classes('ghost-btn')

                        refresh_controls()

                # ---- Validate ----
                with ui.tab_panel(validate_tab).classes('p-0'):
                    with ui.card().classes('glass w-full p-6 gap-4'):
                        ui.label('Verify').classes('section-title')
                        kind_select = ui.select(options=VALIDATE_KINDS, value='personnummer',
                                                label='Validate').classes('w-64')
                        value_input = ui.input('Value').classes('w-full')
                        result_label = ui.label('').classes('text-lg font-semibold')

                        def do_validate():
                            kind, value = kind_select.value, value_input.value or ''
                            if kind == 'personnummer':
                                ok = sc.validate_personnummer(value)
                                result_label.text = f'{"✓ VALID" if ok else "✗ INVALID"} personnummer'
                                result_label.classes(replace='text-lg font-semibold '
                                                     + ('text-positive' if ok else 'text-negative'))
                            elif kind in ('luhn', 'creditcard'):
                                digits = ''.join(c for c in value if c.isdigit())
                                ok = bool(digits) and sc.luhn_is_valid(digits)
                                label = 'credit card' if kind == 'creditcard' else 'Luhn checksum'
                                result_label.text = f'{"✓ VALID" if ok else "✗ INVALID"} {label}'
                                result_label.classes(replace='text-lg font-semibold '
                                                     + ('text-positive' if ok else 'text-negative'))
                            else:  # password
                                strength, score, feedback = sc.check_password_strength(value)
                                msg = f'Strength: {strength} ({score}/6)'
                                if feedback:
                                    msg += ' — ' + ', '.join(feedback)
                                result_label.text = msg
                                result_label.classes(replace='text-lg font-semibold text-info')

                        ui.button('Validate', on_click=do_validate).props('unelevated').classes('neon-btn')

                # ---- History ----
                with ui.tab_panel(history_tab).classes('p-0'):
                    with ui.card().classes('glass w-full p-6 gap-4'):
                        ui.label('Recent').classes('section-title')
                        history_columns = [
                            {'name': 'timestamp', 'label': 'Timestamp', 'field': 'timestamp', 'align': 'left'},
                            {'name': 'type', 'label': 'Type', 'field': 'type'},
                            {'name': 'length', 'label': 'Length', 'field': 'length'},
                            {'name': 'byte_size', 'label': 'Bytes', 'field': 'byte_size'},
                            {'name': 'string', 'label': 'Value', 'field': 'string', 'align': 'left'},
                        ]
                        history_table = ui.table(columns=history_columns, rows=[], row_key='timestamp').classes('w-full')

                        def refresh_history():
                            history_table.rows = list(reversed(sc.load_history()))

                        ui.button('Refresh history', on_click=refresh_history).props('flat').classes('ghost-btn')
                        refresh_history()


build_ui()

if __name__ in {'__main__', '__mp_main__'}:
    native = os.environ.get('STRINGCREATOR_GUI_NATIVE', '1') != '0'
    ui.run(title='StringCreator', favicon='assets/favicon.svg', native=native, reload=False)
