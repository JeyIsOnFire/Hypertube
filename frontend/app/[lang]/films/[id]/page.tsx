
export default async function Page({params, }: {params: Promise<{ id: string }>}) {

  return <div>params{params.id}</div>

}
