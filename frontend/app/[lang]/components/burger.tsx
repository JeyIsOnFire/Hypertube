import React from 'react';
import styles from './burger.module.css';
import translations from '@/locales';

const Burger = () => {
  const [isOpen, setIsOpen] = React.useState(false);
  const t = translations['en'];

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
        <div className={styles.nav}>
        <a href="#">{t.home}</a>
        <a href="#">{t.movies}</a>
        <a href="#">{t.shows}</a>
        <a href="#">{t.trending}</a>
        <a href="#">{t.myaccount}</a>
        </div>
      </div>

      {isOpen && (
          <div className={styles.overlay} onClick={toggleMenu}></div>
      )}

    </>
  );
};

export default Burger;
