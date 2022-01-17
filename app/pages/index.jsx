import Head from 'next/head';
import styles from '../styles/Index.module.css';
import Main from '../components/main';
import { Button, DropdownButton, Dropdown } from 'react-bootstrap';
import { Fonts, Gear } from 'react-bootstrap-icons';
import { Modal } from 'react-bootstrap';
import { useState, useEffect } from 'react';
import { localIP } from '../components/config';
import Slider from '@mui/material/Slider';
import { ChromePicker } from 'react-color';
import ColorButton from '../components/ColorButton';

export default function Home() {
    // Set the state variable for the modal
    const [modalOpen, setModalOpen] = useState(false);
    const [settings, setSettings] = useState({});
    const [fonts, setFonts] = useState([]);
    const [activeFont, setActiveFont] = useState();
    const [brightness, setBrightness] = useState();
    const [staticColor, setStaticColor] = useState();

    const handleModalOpen = () => setModalOpen(true);
    const handleModalClose = () => setModalOpen(false);

    function changeActiveFont(x) {
        setActiveFont(settings.font_dict[x.toString()])
        let settings_copy = Object.assign({}, settings);
        settings_copy.active_font = settings.font_dict[x.toString()];
        setSettings(settings_copy);
    }

    function changeBrightness(value) {
        setBrightness(value);
        let settings_copy = Object.assign({}, settings);
        settings_copy.brightness = value;
        setSettings(settings_copy);
    }

    function changeStaticColor(color, event) {
        setStaticColor(color.rgb)
        let settings_copy = Object.assign({}, settings);
        settings_copy.staticColor = color.rgb;
        setSettings(settings_copy);
    }

    function addFontDropdowns(data) {
        return (
            fonts.map((x, i) => <Dropdown.Item key={i} onClick={() => changeActiveFont(x)}>{x}</Dropdown.Item>)
        )
    }

    function sendSettings() {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(settings)
        };
        fetch('http://' + localIP + ':5000/api/settings', requestOptions);
        handleModalClose();
    }

    useEffect(() => {
        fetch('http://' + localIP + ':5000/api/settings')
            .then(res => res.json())
            .then(data => {
                setSettings(data);
                setFonts(Object.keys(data.font_dict));
                setActiveFont(data.active_font);
                setBrightness(data.brightness);
                setStaticColor(data.staticColor);
            });
    }, [])

    return (
        <div className={styles.container}>
            <Head>
                <title>Retro Magic Board</title>
            </Head>
            <div className={styles.menuBar}>
            <Button className={styles.settingsButton} variant='outline-dark' onClick={handleModalOpen}>
                <Gear />
            </Button>
            </div>
            <div className={styles.titleBar}>
                <h1 className={styles.title}>Magic Color Board</h1>
                <div className={styles.subtitle}>A board of wonders</div>
                <Main className={styles.main}/>
            </div>

            <Modal show={modalOpen} fullscreen="true" onHide={handleModalClose} className={styles.settingsModal} dialogClassName={styles.settingsModal} contentClassName={styles.settingsContent} backdropClassName={styles.settingsBackdrop} fullscreen={true} scrollable={true} centered>
                <Modal.Header closeButton>
                    <Modal.Title>Retroboard Settings</Modal.Title>
                </Modal.Header>
                <Modal.Body className={styles.settingsBody}>
                    <div className={styles.settingsContainer}>
                        <DropdownButton id='font-dropdown' title='Font Selection'>
                        {addFontDropdowns()}
                        </DropdownButton>
                    </div>
                    <div className={styles.settingsContainer}>Active Font Path: {activeFont}</div>
                    <div className={styles.settingsContainer}>Brightness: <Slider className={styles.brightnessSlider} value={brightness} aria-label='default' valueLabelDisplay='auto' sx={{width: 200}} onChangeCommitted={(e, val) => changeBrightness(val)} /></div>
                    {/* <div>Color: <ChromePicker color={staticColor} onChange={(color, event) => setStaticColor(color)} onChangeComplete={changeStaticColor} disableAlpha={true}/></div> */}
                    <div className={styles.settingsContainer}>Font Color: <ColorButton staticColor={staticColor} setStaticColor={setStaticColor} changeStaticColor={changeStaticColor} /></div>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant='outline-dark' onClick={handleModalClose}>
                        Close
                    </Button>
                    <Button variant='outline-dark' onClick={sendSettings}>
                        Save Changes
                    </Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
}
