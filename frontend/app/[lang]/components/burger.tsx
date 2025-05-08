import React from 'react';
import styles from './burger.module.css';
import translations from '@/locales';

const Burger = () => {
  const [isOpen, setIsOpen] = React.useState(false);
  const [isSearching, setIsSearching] = React.useState(false);
  const t = translations['en'];

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const toggleSearch = () => {
    setIsSearching(!isSearching);
  }
  
  return (
    <>
      <div className={styles.row}>

        <div className={styles.row2}>
          <a><svg onClick={toggleSearch} className={styles.searchIcon} xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 50 50" width="50px" height="50px">
            <path d="M 21 3 C 11.601563 3 4 10.601563 4 20 C 4 29.398438 11.601563 37 21 37 C 24.355469 37 27.460938 36.015625 30.09375 34.34375 L 42.375 46.625 L 46.625 42.375 L 34.5 30.28125 C 36.679688 27.421875 38 23.878906 38 20 C 38 10.601563 30.398438 3 21 3 Z M 21 7 C 28.199219 7 34 12.800781 34 20 C 34 27.199219 28.199219 33 21 33 C 13.800781 33 8 27.199219 8 20 C 8 12.800781 13.800781 7 21 7 Z"/>
          </svg></a>
          <a><svg className={styles.logoutIcon} width="30px" height="30px" viewBox="0 0 512 512" >
            <path d="m400 54.1c63 45 104 118.6 104 201.9 0 136.8-110.8 247.7-247.5 248-136.5.3-248.3-111-248.5-247.6-.1-83.3 40.9-157.1 103.8-202.2 11.7-8.3 28-4.8 35 7.7l15.8 28.1c5.9 10.5 3.1 23.8-6.6 31-41.5 30.8-68 79.6-68 134.9-.1 92.3 74.5 168.1 168 168.1 91.6 0 168.6-74.2 168-169.1-.3-51.8-24.7-101.8-68.1-134-9.7-7.2-12.4-20.5-6.5-30.9l15.8-28.1c7-12.4 23.2-16.1 34.8-7.8zm-104 209.9v-240c0-13.3-10.7-24-24-24h-32c-13.3 0-24 10.7-24 24v240c0 13.3 10.7 24 24 24h32c13.3 0 24-10.7 24-24z" />
          </svg></a>
        </div>

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
