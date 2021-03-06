import React from 'react';
import { useState, useEffect } from 'react';
import styles from '../styles/SettingsDialog.module.css';
import ColorButton from './ColorButton';
import { Dialog, DialogContent, DialogTitle, DialogActions, Button, Slider, TextField, Autocomplete, Chip } from '@mui/material';
import { localIP } from './config';
import GradientButton from './GradientButton';

const initialPallet = [
    { offset: '0.00', color: 'rgb(238, 241, 11)' },
    { offset: '1.00', color: 'rgb(126, 32, 207)' },
];

export default function SettingsDialog(props) {
    const [fonts, setFonts] = useState([]);
    const [activeFont, setActiveFont] = useState();
    const [brightness, setBrightness] = useState();
    const [staticColor, setStaticColor] = useState();
    const [colorMode, setColorMode] = useState();
    const [scroll, setScroll] = React.useState('paper');
    const [gradPalette, setGradPalette] = useState(initialPallet);

    const colorModeList = ['static', 'gradient'];

    function changeActiveFont(e, val) {
        if (val != null) {
            setActiveFont(val);
            let settings_copy = Object.assign({}, props.settings);
            settings_copy.main.active_font = val;
            props.setSettings(settings_copy);
        }
    }

    function changeBrightness(value) {
        setBrightness(value);
        let settings_copy = Object.assign({}, props.settings);
        settings_copy.main.brightness = value;
        props.setSettings(settings_copy);
    }

    function changeStaticColor(color, event) {
        setStaticColor(color.rgb);
        let settings_copy = Object.assign({}, props.settings);
        settings_copy.main.static_color = color.rgb;
        props.setSettings(settings_copy);
    }

    function changeColorMode(e, val) {
        if (val != null) {
            setColorMode(val);
            let settings_copy = Object.assign({}, props.settings);
            settings_copy.main.color_mode = val;
            props.setSettings(settings_copy);
        }
    }

    function changeGradPalette(grad) {
        var palette = [];
        for (const c of grad) {
            const clr = 'rgb(' + c.r + ', ' + c.g + ', ' + c.b + ')';
            palette.push({offset: String(c.offset), color: clr})
        }
        setGradPalette(palette);
    }

    function parseGradPalette(grad) {
        let settings_copy = Object.assign({}, props.settings);
        var gradient = []
        for (const c of grad) {
            const rgb = c.color.replace(/[^\d,]/g, '').split(',');
            const offset = parseFloat(c.offset);
            gradient.push({offset: offset, r: parseInt(rgb[0]), g: parseInt(rgb[1]), b: parseInt(rgb[2])});
        }
        settings_copy.main.gradient = gradient;
        props.setSettings(settings_copy);
    }

    function updateGradPalette(grad) {
        setGradPalette(grad);
        parseGradPalette(grad);
    }

    function updateLocalIP(e) {
        const ip = e.target.value;
        props.setLocalSettingsIP(ip);
        props.setResetSettings(!props.resetSettings)
    }
    
    function sendSettings() {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(props.settings),
        };
        fetch('http://' + props.localSettingsIP + '/api/settings', requestOptions);
        props.handleMainSettingsClose();
    }

    useEffect(() => {
        fetch('http://' + props.localSettingsIP + '/api/settings')
            .then((res) => res.json())
            .then((data) => {
                props.setSettings(data);
                setFonts(Object.keys(data.main.font_dict));
                setActiveFont(data.main.active_font);
                setBrightness(data.main.brightness);
                setStaticColor(data.main.static_color);
                setColorMode(data.main.color_mode);
                changeGradPalette(data.main.gradient);
            });
    }, [props.resetSettings]);

    return (
        <div className={styles.container}>
            <Dialog
                open={props.mainSettingsOpen}
                onClose={props.handleMainSettingsClose}
                scroll={scroll}
                aria-labelledby="scroll-dialog-title"
                aria-describedby="scroll-dialog-description"
                fullScreen={true}
                className={styles.dialog}
            >
                <DialogTitle>Retroboard Settings</DialogTitle>
                <DialogContent className={styles.settingsBody}>
                    <div className={styles.settingsContainer}>
                        <Autocomplete
                            disablePortal
                            className={styles.textBox}
                            id='font-selector'
                            options={fonts}
                            sx={{ width: 200 }}
                            onChange={(e, val) => changeActiveFont(e, val)}
                            renderInput={(params) => (
                                <TextField {...params} label='Font' />
                            )}
                        />
                        <Chip label={activeFont} variant='outlined' />
                    </div>
                    <div className={styles.settingsContainer}>
                        Brightness:{' '}
                        <Slider
                            className={styles.brightnessSlider}
                            value={brightness}
                            aria-label='default'
                            valueLabelDisplay='auto'
                            sx={{ width: 200 }}
                            onChange={(e, val) =>
                                changeBrightness(val)
                            }
                        />
                    </div>
                    <div className={styles.settingsContainer}>
                        <Autocomplete
                            disablePortal
                            className={styles.textBox}
                            id='color-mode-selector'
                            options={colorModeList}
                            sx={{ width: 200 }}
                            onChange={(e, val) => changeColorMode(e, val)}
                            renderInput={(params) => (
                                <TextField {...params} label='Color Mode' />
                            )}
                        />
                        <Chip label={colorMode} variant='outlined' />
                    </div>
                    {(() => {
                        if (colorMode == 'static') {
                            return (
                                <div className={styles.settingsContainer}>
                                    Static Font Color:{' '}
                                    <ColorButton
                                        color={staticColor}
                                        setColor={setStaticColor}
                                        changeColor={changeStaticColor}
                                    />
                                </div>
                            );
                        } else if (colorMode == 'gradient') {
                            return (
                                <div className={styles.settingsContainer}>
                                    Gradient Picker: 
                                    <GradientButton 
                                        gradPalette={gradPalette}
                                        setGradPalette={setGradPalette}
                                        updateGradPalette={updateGradPalette}
                                        />
                                </div>  
                            );
                        }
                    })()}
                    <div className={styles.settingsContainer}>
						<TextField className={styles.textBox} sx={{ width: 200 }} id='local-ip' label='Local-IP' onChange={(e) => updateLocalIP(e)}/>
						<Chip label={props.localSettingsIP} variant='outlined' />
					</div>
                </DialogContent>
                <DialogActions>
                    <Button
                        className={styles.button}
                        variant='outlined'
                        color='error'
                        onClick={() => props.setResetSettings(!props.resetSettings)}
                    >
                        Reset
                    </Button>
                    <Button
                        className={styles.button}
                        variant='outlined'
                        onClick={props.handleMainSettingsClose}
                    >
                        Close
                    </Button>
                    <Button 
                    className={styles.button}
                    variant='outlined' 
                    color='success'
                    onClick={sendSettings}>
                        Save Changes
                    </Button>
                </DialogActions>
            </Dialog>
        </div>
    );
}
