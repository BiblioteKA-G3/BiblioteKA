<h1 align="center">:file_cabinet: BiblioteKA</h1>

## :memo: Descrição

O Projeto BiblioteKa, visa demonstrar uma aplicação em Backend, onde foram trabalhadas softskills, como trabalho em grupo, liderança, organização e gestão de prazos, contendo todos os conhecimentos adquiridos até o momento no módulo 5. Esta aplicação simula um sistema de biblioteca, onde um usuário, sendo estudante ou colaborador, tem acessos à um acervo de livros disponíveis para empréstimo.

## :books: Funcionalidades

<div>
  <ul>
    <li>
      <h2 size="16px">Empréstimo de Livros:</h2>
  <p size="14px">Cada livro pode ser emprestado por um período fixo de tempo.</p>
    </li>
    <li>
      <h2 size="16px">Devolução de Livros:</h2>
 <ol>
        <li>Todos os livros emprestados possuem uma data de retorno;</li>
        <li>Caso a devolução caia em um fim de semana (sábado ou domingo), sua a data de retorno é modificada para o próximo dia útil;
        </li>
        <li>Caso o estudante não devolva o livro até o prazo estipulado, ele é impedido (bloqueado) de solicitar outros empréstimos.</li>
      </ol>
    </li>
    <li>
      <h2 size="16px">Bloqueio de Novos Empréstimos:</h2>
      <p size="14px">Se um estudante não efetuar a devolução dos livros no prazo estipulado, ele não pode pegar mais livros emprestads até completar a devolução dos anteriores. Após completar as devoluções pendentes, o bloqueio permanece por alguns dias.</p>
    </li>
    <li>
      <h2 size="16px">Usuários:</h2>
      <p size="14px">A aplicação possui dois usuários: estudante e colaborador. Usuários não autenticados podem acessar a plataforma para visualizar informações sobre os livros, como disponibilidade, título, etc.</p>
      <h3>Para o usuário ESTUDANTE, seguem as seguintes permissões:</h3>
      <ol>
        <li>Ver seu próprio histórico de livros emprestados;</li>
        <li>Obter informações sobre livros;</li>
        <li>Solicitar um empréstimo de livro, caso este não esteja bloqueado.</li>
        <li>Seguir" um livro a fim de receber notificações no email conforme a disponibilidade/status do livro.</li>
      </ol>
      <h3>Para o usuário COLABORADOR, seguem as seguintes permissões:</h3>
      <ol>
        <li>Cadastrar novos livros;</li>
        <li>Emprestar livros;</li>
        <li>Verificar o histórico de empréstimo de cada estudante;</li>
        <li>Verificar status do estudante (se está bloqueado não pode emprestar uma nova cópia durante determinado tempo).</li>
      </ol>
    </li>
 </ul>
</div>

## :memo: Models

<p size="14px">users, books, copies, loans, follows.</p>

## :wrench: Feramentas utilizadas

- Tecnologias:
  - Python;
  - Django;
- Bibliotecas:
- djangorestframework;
- djangorestframework-simplejwt;
- drf-spectacular;
- ipdb;
- ipython;
- python-dotenv;
- gunicorn;
- psycopg2-binary;
- 'whitenoise[brotli]';
- dj-database-url.
- Ferramentas:
  - VsCode;
  - Render;
  - Swagger
  - black

## :rocket: Rodando o projeto

Para rodar o repositório é necessário clonar o mesmo, e dar o seguinte comando para iniciar o projeto:

```
python -m venv venv - Para criar a varável de ambiente
```

```
pip install -r  requirements.txt - Para instalar o pacote de dependeências da aplicação para uso no ambiente virtual.
```

```
pip freeze > requirements.txt  - Para atualizar o pacote de dependências e toda vez que uma lib nova for instalada no ambiente virtual.
```

<p size="18px">A documentação contendo as rotas da aplicação, pode ser visulizada através deste <a href="https://biblioteka-cja7.onrender.com/api/docs/">link</a></p>

## :handshake: Autores

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/alexandra86">
        <sub>
          <b>Alexandra Miranda</b>
        </sub>
      </a>
    </td>
      <td align="center">
      <a href="https://github.com/DaViolet">
        <sub>
          <b>Davi Fernandes</b>
        </sub>
      </a>
    </td>
     <td align="center">
      <a href="https://github.com/DiegoAndreLeffa">
        <sub>
          <b>Diego André</b>
        </sub>
      </a>
    </td>
     <td align="center">
      <a href="https://github.com/LucasMires">
        <sub>
          <b>Lucas Mires</b>
        </sub>
      </a>
    </td>
     
</table>

## :dart: Status do projeto

\*Finalizado
