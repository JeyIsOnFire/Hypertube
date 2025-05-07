import Landing from './landing/page';

const Home = ({ params }: { params: { lang: string }}) => {

  return (
    <div>
      <Landing params={params}/>
    </div>
  );
};

export default Home;
