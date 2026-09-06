const express = require('express');
const axios = require('axios');
const path = require('path');
require('dotenv').config();

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Rota protegida SASCAR (As credenciais ficam seguras no servidor)
app.get('/api/sascar/posicoes', async (req, res) => {
    try {
        // Exemplo de chamada real usando as variáveis de ambiente da nuvem
        /* 
        const response = await axios.post('URL_WSDL_SASCAR', {
            usuario: process.env.SASCAR_USUARIO,
            senha: process.env.SASCAR_SENHA
        });
        return res.json(response.data);
        */
        
        // Retorno estruturado para validação imediata
        res.json([
            { placa: 'ABC-1234', lat: -23.5505, lon: -46.6333, ignicao: true, vel: 65, odometro: 150200, dataHora: new Date().toISOString(), cidade: 'São Paulo', uf: 'SP' },
            { placa: 'XYZ-9876', lat: -22.9068, lon: -43.1729, ignicao: true, vel: 85, odometro: 89000, dataHora: new Date().toISOString(), cidade: 'Rio de Janeiro', uf: 'RJ' }
        ]);
    } catch (error) {
        res.status(500).json({ error: 'Erro ao consultar SASCAR' });
    }
});

// Rota protegida CTA
app.get('/api/cta/abastecimentos', async (req, res) => {
    try {
        res.json([
            { placa: 'ABC-1234', bomba: '3654', vol: 500.34, odometro: 150200, dist: 907, media: 1.81, dataInicio: new Date().toISOString() }
        ]);
    } catch (error) {
        res.status(500).json({ error: 'Erro ao consultar CTA' });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Servidor rodando na porta ${PORT}`));