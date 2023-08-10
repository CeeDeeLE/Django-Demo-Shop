import { sql } from "@vercel/postgres";
// https://vercel.com/dashboard/stores/postgres/store_WqZLg4HFk4juA5mP/guides
export default async function Cart({ params }) {
  const { rows } = await sql`SELECT * from CARTS where user_id=${params.user}`;

  return (
    <div>
      {rows.map((row) => (
        <div key={row.id}>
          {row.id} - {row.quantity}
        </div>
      ))}
    </div>
  );
}
