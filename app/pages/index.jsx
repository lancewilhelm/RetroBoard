import Head from 'next/head';
import styles from '../styles/Index.module.css';
import { Button, Menu, MenuItem } from '@mui/material';
import { useState, useEffect } from 'react';
import SettingsOutlinedIcon from '@mui/icons-material/SettingsOutlined';
import SettingsDialog from '../components/SettingsDialog';
import AppSettings from '../components/AppSettings';
import { localIP } from '../components/config';

export default function Home() {
	// Set the state variable for the modal
	const [settings, setSettings] = useState({});
	const [resetSettings, setResetSettings] = useState(false);
	const [mainSettingsOpen, setMainSettingsOpen] = useState(false);
	const [appSettingsOpen, setAppSettingsOpen] = useState(false);
    const [localSettingsIP, setLocalSettingsIP]= useState(localIP);
	const [appsList, setAppsList] = useState([]);
	const [contextMenu, setContextMenu] = useState(null);
	const [whichMenu, setWhichMenu] = useState(null);

	const handleAppSettingsOpen = () => setAppSettingsOpen(true);
	const handleAppSettingsClose = () => setAppSettingsOpen(false);

	const handleMainSettingsOpen = () => setMainSettingsOpen(true);
	const handleMainSettingsClose = () => setMainSettingsOpen(false);

	async function sendCommand(command) {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({app: command})
        };
        fetch('http://' + localSettingsIP + '/api/app', requestOptions);
    }

	function renderAppButtons() {
		return (
			appsList.map((x,i) => <Button className={styles.btn} key={i} id={x} variant='outlined' onContextMenu={handleContextMenu} style={{cursor: 'context-menu'}}onClick={() => sendCommand(x)}>{x}</Button>)
		)
	}

	function handleContextMenu(event) {
		event.preventDefault();
		setWhichMenu(event.target.id);
		setContextMenu(
			contextMenu === null 
			? {
				mouseX: event.clientX,
				mouseY: event.clientY,
			}
			:
			null,
		);
	};

	function handleMenuSelect() {
		handleAppSettingsOpen();
		setContextMenu(null);
		// setWhichMenu(null);
	}

	useEffect(() => {
        fetch('http://' + localSettingsIP + '/api/settings')
            .then((res) => res.json())
            .then((data) => {
                setSettings(data);
				setAppsList(data.main.apps_list);
            });
    }, [resetSettings]);

	return (
		<div className={styles.pagecontainer}>
			<Head>
				<title>Retro Magic Board</title>
			</Head>
			<div className={styles.menuBar}>
				<Button
					className={styles.settingsButton}
					variant=''
					onClick={handleMainSettingsOpen}
				>
					<SettingsOutlinedIcon />
				</Button>
			</div>
			<div className={styles.titleBar}>
				<h1 className={styles.title}>Magic Color Board</h1>
				<div className={styles.subtitle}>A board of wonders</div>
				<div className={styles.maincontainer}>
					{renderAppButtons()}
					<Button
						className={styles.btn}
						variant='outlined'
						onClick={() => sendCommand('Clear')}
					>
						Clear
					</Button>

					<Menu open={contextMenu !== null} onClose={() => setContextMenu(null)} anchorReference='anchorPosition' anchorPosition={contextMenu !== null ? {top: contextMenu.mouseY, left: contextMenu.mouseX } : undefined}>
						<MenuItem onClick={handleMenuSelect}>Settings</MenuItem>
					</Menu>

					<AppSettings
						appSettingsOpen={appSettingsOpen}
						handleAppSettingsOpen={handleAppSettingsOpen}
						handleAppSettingsClose={handleAppSettingsClose}
						settings={settings}
						setSettings={setSettings}
						resetSettings={resetSettings}
						setResetSettings={setResetSettings}
						app={whichMenu}
					/>
				</div>
			</div>

			<SettingsDialog
				mainSettingsOpen={mainSettingsOpen}
				handleMainSettingsOpen={handleMainSettingsOpen}
				handleMainSettingsClose={handleMainSettingsClose}
				settings={settings}
				setSettings={setSettings}
				resetSettings={resetSettings}
				setResetSettings={setResetSettings}
				localSettingsIP={localSettingsIP}
				setLocalSettingsIP={setLocalSettingsIP}
			/>
		</div>
	);
}
