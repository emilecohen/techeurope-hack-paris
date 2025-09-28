'use client';

import { useRouter } from 'next/navigation';
import React, { useState } from 'react';
import { encodePassphrase, generateRoomId, randomString } from '@/lib/client-utils';
import styles from '../styles/Home.module.css';

function StartMeeting() {
  const router = useRouter();
  const [e2ee, setE2ee] = useState(false);
  const [sharedPassphrase, setSharedPassphrase] = useState(randomString(64));

  const startMeeting = () => {
    if (e2ee) {
      router.push(`/rooms/${generateRoomId()}#${encodePassphrase(sharedPassphrase)}`);
    } else {
      router.push(`/rooms/${generateRoomId()}`);
    }
  };

  return (
    <div className="mt-8 bg-card p-6 rounded-xl shadow-[var(--shadow-card)] border">
      <button
        className="w-full px-8 py-4 bg-primary hover:bg-primary/90 text-primary-foreground font-semibold rounded-lg transition-colors duration-300"
        onClick={startMeeting}
      >
        Start Meeting
      </button>
    </div>
  );
}

export default function Page() {
  return (
    <div className="min-h-screen bg-background">
      <div className="pt-24 pb-12">
        <div className="container mx-auto px-6">
          <main className={`${styles.main} min-h-screen flex flex-col items-center justify-center`}>
            <div className="bg-card p-8 rounded-xl shadow-[var(--shadow-card)] max-w-4xl mx-auto border">
              <img
                src="/images/news.png"
                alt="NewsCaster AI"
                width="360"
                height="100"
                className="mx-auto block"
              />
              <h2 className="text-center text-xl font-normal text-foreground mt-4">
                <strong>NewsCaster AI</strong> – An open-source AI news avatar platform built with{' '}
                <a
                  href="https://github.com/livekit/components-js?ref=meet"
                  rel="noopener"
                  className="text-primary hover:text-primary/80 transition-colors"
                >
                  LiveKit&nbsp;Components
                </a>
                ,{' '}
                <a
                  href="https://livekit.io/cloud?ref=meet"
                  rel="noopener"
                  className="text-primary hover:text-primary/80 transition-colors"
                >
                  LiveKit&nbsp;Cloud
                </a>{' '}
                and Next.js, delivering video-based news and updates in real time.
              </h2>
            </div>
            <StartMeeting />
          </main>

          <footer className="w-full p-6 text-center text-muted-foreground border-t border-border mt-12">
            Hosted on{' '}
            <a
              href="https://livekit.io/cloud?ref=meet"
              rel="noopener"
              className="text-primary hover:text-primary/80 transition-colors"
            >
              LiveKit Cloud
            </a>
            . Source code on{' '}
            <a
              href="https://github.com/livekit/meet?ref=meet"
              rel="noopener"
              className="text-primary hover:text-primary/80 transition-colors"
            >
              GitHub
            </a>
            .
          </footer>
        </div>
      </div>
    </div>
  );
}
