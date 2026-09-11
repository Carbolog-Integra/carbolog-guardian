export default async function handler(req, res) {
    const SUPABASE_URL = process.env.SUPABASE_URL;
    const SUPABASE_KEY = process.env.SUPABASE_KEY;

    const headersSupabase = {
        'apikey': SUPABASE_KEY,
        'Authorization': `Bearer ${SUPABASE_KEY}`,
        'Content-Type': 'application/json'
    };

    const tabela = req.query.tabela || 'posicoes_sascar';

    if (req.method === 'GET') {
        try {
            const resposta = await fetch(`${SUPABASE_URL}/rest/v1/${tabela}?select=*`, {
                method: 'GET',
                headers: headersSupabase
            });
            if (!resposta.ok) {
                const erroTxt = await resposta.text();
                return res.status(resposta.status).json({ error: erroTxt });
            }
            const dados = await resposta.json();
            return res.status(200).json(dados);
        } catch (e) {
            return res.status(500).json({ error: e.message });
        }
    }

    if (req.method === 'POST') {
        try {
            const resposta = await fetch(`${SUPABASE_URL}/rest/v1/${tabela}`, {
                method: 'POST',
                headers: { 
                    ...headersSupabase, 
                    'Prefer': 'resolution=merge-duplicates' 
                },
                body: JSON.stringify(req.body)
            });
            if (!resposta.ok) {
                const erroTxt = await resposta.text();
                return res.status(resposta.status).json({ error: erroTxt });
            }
            return res.status(200).json({ status: 'Sucesso' });
        } catch (e) {
            return res.status(500).json({ error: e.message });
        }
    }

    if (req.method === 'DELETE') {
        try {
            const id = req.query.id;
            const resposta = await fetch(`${SUPABASE_URL}/rest/v1/${tabela}?id=eq.${id}`, {
                method: 'DELETE',
                headers: headersSupabase
            });
            if (!resposta.ok) {
                const erroTxt = await resposta.text();
                return res.status(resposta.status).json({ error: erroTxt });
            }
            return res.status(200).json({ status: 'Removido' });
        } catch (e) {
            return res.status(500).json({ error: e.message });
        }
    }

    return res.status(405).json({ error: 'Método não permitido' });
}
