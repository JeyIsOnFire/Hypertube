import React from 'react';
import styles from './burger.module.css';
import translations from '@/locales';
import LanguageSwitcher from './language-switcher';
import { Monoton } from 'next/font/google';
import Link from "next/link";

const monoton = Monoton({ subsets: ['latin'], weight: '400' });

type HeaderProps = {
  lang: 'fr' | 'en';
}

const Burger = ({ lang }: HeaderProps) => {
  const [isOpen, setIsOpen] = React.useState(false);
  const t = translations[lang];

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      <div 
        role="button"
        aria-expanded={isOpen}
        aria-label="Toggle Menu"
        className={`${styles.container} ${isOpen ? styles.change : ''}`}
        onClick={toggleMenu}
      >
        <div className={styles.bar1}></div>
        <div className={styles.bar2}></div>
        <div className={styles.bar3}></div>
      </div>

      <div className={`${styles.slideMenu} ${isOpen ? styles.open: ''}`}>
        <div className={styles.languageSwitcher}>
          <LanguageSwitcher />
        </div>
        <div className={`${monoton.className} ${styles.nav}`}>
        <Link href="/">{t.home}</Link>
        <a href="#">{t.movies}</a>
        <a href="#">{t.shows}</a>
        <Link href="/account/">{t.myaccount}</Link>
        </div>
      </div>

      {isOpen && (
          <div className={styles.overlay} onClick={toggleMenu}></div>
      )}
    </>
  );
};

export default Burger;
