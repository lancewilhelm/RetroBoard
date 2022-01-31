import React from 'react';
import { useState, useEffect } from 'react';
import styles from '../styles/SettingsDialog.module.css';
import ColorButton from './ColorButton';
import { Dialog, DialogContent, DialogTitle, DialogActions, Button, Slider, TextField, Autocomplete, Chip } from '@mui/material';
import { localIP } from './config';
import GradientButton from './GradientButton';

export default function SettingsDialog(props) {
    const [settings, setSettings] = useState({});
    const [reset, setReset] = useState(false);
    const [fonts, setFonts] = useState([]);
    const [activeFont, setActiveFont] = useState();
    const [brightness, setBrightness] = useState();
    const [staticColor, setStaticColor] = useState();
    const [colorMode, setColorMode] = useState();
    const [gradStartColor, setGradStartColor] = useState();
    const [gradEndColor, setGradEndColor] = useState();
    const [scroll, setScroll] = React.useState('paper');

    const colorModeList = ['static', 'gradient'];

    function changeActiveFont(e, val) {
        if (val != null) {
            setActiveFont(val);
            let settings_copy = Object.assign({}, settings);
            settings_copy.active_font = val;
            setSettings(settings_copy);
        }
    }

    function changeBrightness(value) {
        setBrightness(value);
        let settings_copy = Object.assign({}, settings);
        settings_copy.brightness = value;
        setSettings(settings_copy);
    }

    function changeStaticColor(color, event) {
        setStaticColor(color.rgb);
        let settings_copy = Object.assign({}, settings);
        settings_copy.static_color = color.rgb;
        setSettings(settings_copy);
    }

    function changeGradStartColor(color, event) {
        setGradStartColor(color.rgb);
        let settings_copy = Object.assign({}, settings);
        settings_copy.grad_start_color = color.rgb;
        setSettings(settings_copy);
    }

    function changeGradEndColor(color, event) {
        setGradEndColor(color.rgb);
        let settings_copy = Object.assign({}, settings);
        settings_copy.grad_end_color = color.rgb;
        setSettings(settings_copy);
    }

    function changeColorMode(e, val) {
        if (val != null) {
            setColorMode(val);
            let settings_copy = Object.assign({}, settings);
            settings_copy.color_mode = val;
            setSettings(settings_copy);
        }
    }

    function sendSettings() {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(settings),
        };
        fetch('http://' + localIP + ':5000/api/settings', requestOptions);
        props.handleDialogClose();
    }

    useEffect(() => {
        fetch('http://' + localIP + ':5000/api/settings')
            .then((res) => res.json())
            .then((data) => {
                setSettings(data);
                setFonts(Object.keys(data.font_dict));
                setActiveFont(data.active_font);
                setBrightness(data.brightness);
                setStaticColor(data.static_color);
                setColorMode(data.color_mode);
                setGradStartColor(data.grad_start_color);
                setGradEndColor(data.grad_end_color);
            });
    }, [reset]);

    return (
        <div className={styles.container}>
            <Dialog
                open={props.dialogOpen}
                onClose={props.handleDialogClose}
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
                            onChangeCommitted={(e, val) =>
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
                                <div>
                                    <div className={styles.settingsContainer}>
                                        Grad Start Color:{' '}
                                        <ColorButton
                                            color={gradStartColor}
                                            setColor={setGradStartColor}
                                            changeColor={changeGradStartColor}
                                        />
                                    </div>
                                    <div className={styles.settingsContainer}>
                                        Grad End Color:{' '}
                                        <ColorButton
                                            color={gradEndColor}
                                            setColor={setGradEndColor}
                                            changeColor={changeGradEndColor}
                                        />
                                    </div>
                                </div>
                            );
                        }
                    })()}
                    <div className={styles.settingsContainer}>
                        <GradientButton />
                    </div>
                </DialogContent>
                <DialogActions>
                    <Button
                        className={styles.button}
                        variant='outlined'
                        color='error'
                        onClick={() => setReset(!reset)}
                    >
                        Reset
                    </Button>
                    <Button
                        className={styles.button}
                        variant='outlined'
                        onClick={props.handleDialogClose}
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
