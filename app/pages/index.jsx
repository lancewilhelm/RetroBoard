import Head from 'next/head';
import styles from '../styles/Index.module.css';
import { Button, ButtonGroup } from '@mui/material';
import { useState } from 'react';
import SettingsOutlinedIcon from '@mui/icons-material/SettingsOutlined';
import SettingsDialog from '../components/SettingsDialog';
import TickerSettings from '../components/TickerSettings';
import { localIP } from '../components/config';

export default function Home() {
	// Set the state variable for the modal
	const [settings, setSettings] = useState({});
	const [resetSettings, setResetSettings] = useState(false);
	const [mainSettingsOpen, setMainSettingsOpen] = useState(false);
	const [tickerSettingsOpen, setTickerSettingsOpen] = useState(false);

	const handleTickerSettingsOpen = () => setTickerSettingsOpen(true);
	const handleTickerSettingsClose = () => setTickerSettingsOpen(false);

	const handleMainSettingsOpen = () => setMainSettingsOpen(true);
	const handleMainSettingsClose = () => setMainSettingsOpen(false);

	async function sendCommand(command) {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({app: command})
        };
        fetch('http://' + localIP + ':5000/api/app', requestOptions);
    }

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
					<Button
						className={styles.btn}
						variant='outlined'
						onClick={() => sendCommand('clock')}
					>
						Clock
					</Button>
					<Button
						className={styles.btn}
						variant='outlined'
						onClick={() => sendCommand('text_clock')}
					>
						Text Clock
					</Button>
					<Button
						className={styles.btn}
						variant='outlined'
						onClick={() => sendCommand('picture')}
					>
						Picture
					</Button>
					<ButtonGroup variant='outlined' className={styles.btngrp}>
						<Button
							onClick={() => sendCommand('ticker')}
							className={styles.btngrpbtn}
						>
							Ticker
						</Button>
						<Button
							className={styles.btngrpbtn}
							onClick={handleTickerSettingsOpen}
						>
							<SettingsOutlinedIcon fontSize='small' />
						</Button>
					</ButtonGroup>
					<Button
						className={styles.btn}
						variant='outlined'
						onClick={() => sendCommand('solid')}
					>
						Solid
					</Button>
					<Button
						className={styles.btn}
						variant='outlined'
						onClick={() => sendCommand('clear')}
					>
						Clear
					</Button>

					<TickerSettings
						tickerSettingsOpen={tickerSettingsOpen}
						handleTickerSettingsOpen={handleTickerSettingsOpen}
						handleTickerSettingsClose={handleTickerSettingsClose}
						settings={settings}
						setSettings={setSettings}
						resetSettings={resetSettings}
						setResetSettings={setResetSettings}
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
			/>
		</div>
	);
}
