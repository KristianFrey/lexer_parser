processo {
    nome = "Erro 5: Propriedades Essenciais Faltando";
    dono = "Departamento de Testes";
    inicio = ativ1;

    atividades {
        ativ1 {
            tipo = "tarefa";
            tempo = 1;
            custo = 0;
            seguinte = { fim };
        }
    }

    fim = "Processo Encerrado";
}
