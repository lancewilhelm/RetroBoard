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
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import Chip from '@mui/material/Chip';

export default function Home() {
	// Set the state variable for the modal
	const [modalOpen, setModalOpen] = useState(false);
	const [settings, setSettings] = useState({});
	const [fonts, setFonts] = useState([]);
	const [activeFont, setActiveFont] = useState();
	const [brightness, setBrightness] = useState();
	const [staticColor, setStaticColor] = useState();
	const [colorMode, setColorMode] = useState();

	const handleModalOpen = () => setModalOpen(true);
	const handleModalClose = () => setModalOpen(false);

	function changeActiveFont(e, val) {
		if (val != null) {
			setActiveFont(val)
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
		setStaticColor(color.rgb)
		let settings_copy = Object.assign({}, settings);
		settings_copy.static_color = color.rgb;
		setSettings(settings_copy);
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
				setStaticColor(data.static_color);
				setColorMode(data.color_mode);
			});
	}, [])

	const colorModeList = ['static', 'gradient']

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
					<div className={styles.settingsContainer}><Autocomplete disablePortal id='font-selector' options={fonts} sx={{width: 200, marginRight: '10px'}} onChange={(e, val) => changeActiveFont(e, val)} renderInput={(params) => <TextField {...params} label='Font' />} /><Chip label={activeFont} variant='outlined'/></div>
					<div className={styles.settingsContainer}>Brightness: <Slider className={styles.brightnessSlider} value={brightness} aria-label='default' valueLabelDisplay='auto' sx={{width: 200}} onChangeCommitted={(e, val) => changeBrightness(val)} /></div>
					<div className={styles.settingsContainer}>Font Color: <ColorButton staticColor={staticColor} setStaticColor={setStaticColor} changeStaticColor={changeStaticColor} /></div>
					<div className={styles.settingsContainer}><Autocomplete disablePortal id='color-mode-selector' options={colorModeList} sx={{width: 200}} renderInput={(params) => <TextField {...params} label='Color Mode' />} /></div>
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
