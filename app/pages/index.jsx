import Head from 'next/head';
import styles from '../styles/Index.module.css';
import Main from '../components/main';
import { Button } from 'react-bootstrap';
import { Gear } from 'react-bootstrap-icons';
import { useState } from 'react';
import SettingsModal from '../components/SettingsModal';

export default function Home() {
    // Set the state variable for the modal
    const [modalOpen, setModalOpen] = useState(false);

    const handleModalOpen = () => setModalOpen(true);
    const handleModalClose = () => setModalOpen(false);

    return (
        <div className={styles.container}>
            <Head>
                <title>Retro Magic Board</title>
            </Head>
            <div className={styles.menuBar}>
                <Button
                    className={styles.settingsButton}
                    variant='outline-dark'
                    onClick={handleModalOpen}
                >
                    <Gear />
                </Button>
            </div>
            <div className={styles.titleBar}>
                <h1 className={styles.title}>Magic Color Board</h1>
                <div className={styles.subtitle}>A board of wonders</div>
                <Main className={styles.main} />
            </div>

            <SettingsModal
                modalOpen={modalOpen}
                handleModalOpen={handleModalOpen}
                handleModalClose={handleModalClose}
            />
        </div>
    );
}
