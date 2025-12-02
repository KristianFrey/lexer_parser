processo {
    nome = "Erro 3: Destino de Fluxo Inexistente";
    dono = "Departamento de Testes";
    inicio = ativ1;

    atividades {
        ativ1 {
            nome = "Atividade Inicial";
            tipo = "tarefa";
            responsavel = "Funcionário";
            tempo = 1;
            custo = 0;
            seguinte = { atividade_que_nao_existe };
        }

        ativ2 {
            nome = "Atividade 2";
            tipo = "tarefa";
            responsavel = "Funcionário";
            seguinte = { fim };
        }
    }

    fim = "Processo Encerrado";
}
