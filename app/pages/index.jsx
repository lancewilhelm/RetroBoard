import Head from 'next/head';
import styles from '../styles/Index.module.css';
import Main from '../components/main';
import { Button } from '@mui/material';
import { Gear } from 'react-bootstrap-icons';
import { useState } from 'react';
import SettingsDialog from '../components/SettingsDialog';

export default function Home() {
    // Set the state variable for the modal
    const [dialogOpen, setDialogOpen] = useState(false);

    const handleDialogOpen = () => setDialogOpen(true);
    const handleDialogClose = () => setDialogOpen(false);

    return (
        <div className={styles.container}>
            <Head>
                <title>Retro Magic Board</title>
            </Head>
            <div className={styles.menuBar}>
                <Button
                    className={styles.settingsButton}
                    variant=''
                    onClick={handleDialogOpen}
                >
                    <Gear />
                </Button>
            </div>
            <div className={styles.titleBar}>
                <h1 className={styles.title}>Magic Color Board</h1>
                <div className={styles.subtitle}>A board of wonders</div>
                <Main className={styles.main} />
            </div>

            <SettingsDialog
                dialogOpen={dialogOpen}
                handleDialogOpen={handleDialogOpen}
                handleDialogClose={handleDialogClose}
            />
        </div>
    );
}
