# Código blindado contra erros de dados vazios
        try:
            escanteios = res['corners']['avg']['total'] if res['corners'] else 0
            amarelos = res['cards']['yellow']['total'] if res['cards'] else 0
            gols_feitos = res['goals']['for']['average']['total'] if res['goals'] else 0
            gols_sofridos = res['goals']['against']['average']['total'] if res['goals'] else 0
        except (KeyError, TypeError):
            escanteios = 0
            amarelos = 0
            gols_feitos = 0
            gols_sofridos = 0

        btts_vibe = "✅ ALTA" if float(gols_feitos) > 1.0 and float(gols_sofridos) > 0.9 else "❌ BAIXA"
