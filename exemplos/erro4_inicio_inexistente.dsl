processo {
    nome = "Erro 4: Atividade Inicial Inexistente";
    dono = "Departamento de Testes";
    inicio = atividade_que_nao_existe;

    atividades {
        ativ1 {
            nome = "Atividade 1";
            tipo = "tarefa";
            responsavel = "Funcionário";
            tempo = 1;
            custo = 0;
            seguinte = { ativ2 };
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
