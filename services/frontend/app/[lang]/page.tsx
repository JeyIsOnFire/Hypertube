import Landing from './landing/page';

export default async function Home({ params }) {

  const { lang } = await params;
  return (
    <div>
      <Landing lang={lang}/>
    </div>
  );
};

